import psycopg2, sys
from sentence_transformers import SentenceTransformer

DB_CONFIG = {
    "host": "localhost",
    "dbname": "d2021320031",
    "user": "postgres",
    "password": "6215",
    "port": "5432"
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.OperationalError as e:
        print(f"데이터베이스 연결에 실패했습니다: {e}")
        return None

def extract_execution_time(plan_rows):
    for row in plan_rows:
        line = row[0]
        if "Execution Time" in line:
            # e.g., 'Execution Time: 3.456 ms'
            return float(line.split("Execution Time:")[1].replace("ms","").strip())
    return None

def main():
    if len(sys.argv) < 2:
        print("사용법: python rag_project.py <search-key>")
        sys.exit()
    
    key = sys.argv[1]
    print("입력받은 key:", key)

    conn = get_db_connection()
    model = SentenceTransformer("jhgan/ko-sbert-nli")

    if not conn:
        return
    
    with conn.cursor() as cur:
        cur.execute("""
            CREATE INDEX IF NOT EXISTS wiki_embedding_hnsw_idx
            ON wiki USING hnsw (embedding vector_cosine_ops);
        """)
        cur.execute("ANALYZE wiki;")
        query = model.encode(key).tolist()

        sql = """
            SELECT id, title, content,
                   1 - (embedding <=> %s::vector) AS Similarity 
            FROM wiki
            ORDER BY embedding <=> %s::vector
            LIMIT 10;
        """
        cur.execute(sql, (query, query))
        rows = cur.fetchall()
        

        print("\n--- 최종 검색 결과 (가장 유사한 문서 10개) ---")
        for row in rows:
            id, title, content, similarity = row
            print(f"id: {id}, 제목: {title}, 유사도: {similarity}")
            print(f"내용: {content[:120]}...\n")
    
        print("\n--- 성능 비교 ---")

        explain_sql = """
            EXPLAIN ANALYZE SELECT id, title, content,
                   1 - (embedding <=> %s::vector) AS Similarity 
            FROM wiki
            ORDER BY embedding <=> %s::vector
            LIMIT 10;
        """

        cur.execute("SET enable_indexscan=off;")
        cur.execute(explain_sql, (query, query))
        noidx_plan = cur.fetchall()
        noidx_time = extract_execution_time(noidx_plan)
        print(f"인덱스 미사용 시 (순차 스캔 강제): {noidx_time:.4f} ms")
        print(noidx_plan)

        cur.execute("SET enable_indexscan=on;")
        cur.execute(explain_sql, (query, query))
        idx_plan = cur.fetchall()
        idx_time = extract_execution_time(idx_plan)
        print(f"인덱스 사용 시 (인덱스 스캔 우선): {idx_time:.4f} ms\n")
        print(idx_plan)
        

        print(f"결론: 인덱스를 사용했을 때 약 {noidx_time / idx_time:.2f} 배 더 빨라졌습니다.")


    conn.close()

if __name__ == "__main__":
    main()
