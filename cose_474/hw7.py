import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import math
import os

from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data.dataset import random_split


from tqdm import tqdm

import importlib

from datetime import datetime as dt
import time

import imdb_voc



root = './'

# import sentences
importlib.reload(imdb_voc)

# set device
dev = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

"""

You can implement any necessary methods.

"""

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_model,dropout):
        super().__init__()
        self.d_model = d_model
        self.dropout = nn.Dropout(dropout)
        self.scale = 1 / (d_model ** 0.5)
    
    def forward(self, Q, K, V, src_batch_lens):
        scores = torch.matmul(Q, K.transpose(-1, -2))
        scores = scores.mul_(self.scale)
        
        attn_mask = torch.zeros_like(scores, dtype=torch.bool)

        for i, word_len in enumerate(src_batch_lens):
            attn_mask[i, :, :, word_len:] = True
        
            
        scores.masked_fill_(attn_mask, -1e9)

        attn_prob = nn.Softmax(dim=-1)(scores)
        attn_prob = self.dropout(attn_prob)

        context = torch.matmul(attn_prob, V)

        return context

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, d_Q, d_K, d_V, numhead, dropout):    
      super().__init__()
      
      self.numhead = numhead
      self.d_model = d_model
      self.depth = d_model//numhead

      self.W_Q= nn.Linear(d_model, d_Q*numhead)
      self.W_K= nn.Linear(d_model, d_K*numhead)
      self.W_V= nn.Linear(d_model, d_V*numhead)

      self.scaled_dot = ScaledDotProductAttention(d_model,dropout)
      self.W_O= nn.Linear(d_V*numhead, d_model)
      self.dropout = nn.Dropout(dropout)
      
    def forward(self, x_Q, x_K, x_V, src_batch_lens=None):
      batch_size = x_Q.shape[0]

      q = self.W_Q(x_Q).view(batch_size, -1, self.numhead, self.d_model).transpose(1,2)
      k = self.W_Q(x_K).view(batch_size, -1, self.numhead, self.d_model).transpose(1,2)
      v = self.W_Q(x_V).view(batch_size, -1, self.numhead, self.d_model).transpose(1,2)


        
      context = self.scaled_dot(q, k, v, src_batch_lens)
      context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.numhead * self.depth)
      
      out = self.W_O(context)
      out = self.dropout(out)

      return out
  

            

class TF_Encoder_Block(nn.Module):
    def __init__(self, d_model, d_ff, numhead, dropout):    
      super().__init__()
      d= d_model//numhead
      self.mul_att = MultiHeadAttention(d_model,d,d,d,numhead,dropout)
      self.layernorm1 = nn.LayerNorm(d_model,eps=1e-19)
      self.ff = nn.Sequential(
          nn.Linear(d_model,d_ff),
          nn.ReLU(),
          nn.Dropout(dropout),
          nn.Linear(d_ff,d_model),
          nn.Dropout(dropout)
      )
      self.layernorm2 = nn.LayerNorm(d_model,eps=1e-19)
      

    def forward(self, x, src_batch_lens):
      
        output = self.mul_att(x,x,x,src_batch_lens)
        output = self.layernorm1(x+output)
        output = self.ff(output)
        out = self.layernorm2(x+output)
        return out

"""
Positional encoding
PE(pos,2i) = sin(pos/10000**(2i/dmodel))
PE(pos,2i+1) = cos(pos/10000**(2i/dmodel))
"""

def PosEncoding(t_len, d_model):
    i = torch.tensor(range(d_model))
    pos = torch.tensor(range(t_len))
    POS, I = torch.meshgrid(pos, i)
    PE = (1-I % 2)*torch.sin(POS/10**(4*I/d_model)) + (I%2)*torch.cos(POS/10**(4*(I-1)/d_model))
    return PE

class TF_Encoder(nn.Module):
    def __init__(self, vocab_size, d_model,
                 d_ff, numlayer, numhead, dropout):    
        super().__init__()
        
        self.numlayer = numlayer
        self.src_embed  = nn.Embedding(num_embeddings=vocab_size, embedding_dim=d_model)
        self.dropout=nn.Dropout(dropout)
        
        self.n_enc = nn.ModuleList([TF_Encoder_Block(d_model,d_ff,numhead,dropout) for _ in range(numlayer)])

        
    def forward(self, x, src_batch_lens):

      x_embed = self.src_embed(x)
      x = self.dropout(x_embed)
      p_enc = PosEncoding(x.shape[1], x.shape[2]).to(dev)
      x = x + p_enc
        
      for module in self.n_enc:
          x=module(x,src_batch_lens)
      out =x
      return out



"""

main model

"""

class sentiment_classifier(nn.Module):
    
    def __init__(self, enc_input_size, 
                 enc_d_model,
                 enc_d_ff,
                 enc_num_layer,
                 enc_num_head,
                 dropout,
                ):    
        super().__init__()
        
        self.encoder = TF_Encoder(vocab_size = enc_input_size,
                                  d_model = enc_d_model, d_ff=enc_d_ff,
                                  numlayer=enc_num_layer, numhead=enc_num_head,
                                  dropout=dropout)

        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1,None)),
            nn.Dropout(dropout),
            nn.Linear(in_features = enc_d_model, out_features=enc_d_model),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(in_features = enc_d_model, out_features = 1)
        )
          
   
    def forward(self, x, x_lens):
        src_ctx = self.encoder(x, src_batch_lens = x_lens)
        # size should be (b,)
        out_logits = self.classifier(src_ctx).flatten()

        return out_logits

"""

datasets

"""

# Load IMDB dataset
# once the dataset 'imdb_dataset.pt' is build, saves time

imdb_dataset_path = './imdb_dataset.pt'

if os.path.isfile(imdb_dataset_path):
    imdb_dataset = torch.load(imdb_dataset_path)
else:
    imdb_dataset = imdb_voc.IMDB_tensor_dataset()
    torch.save(imdb_dataset, imdb_dataset_path)

train_dataset, test_dataset = imdb_dataset.get_dataset()

split_ratio = 0.85
num_train = int(len(train_dataset) * split_ratio)
split_train, split_valid = random_split(train_dataset, [num_train, len(train_dataset) - num_train])

# Set hyperparam (batch size)
batch_size_trn = 256
batch_size_val = 256
batch_size_tst = 256

train_dataloader = DataLoader(split_train, batch_size=batch_size_trn, shuffle=True)
val_dataloader = DataLoader(split_valid, batch_size=batch_size_val, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size_tst, shuffle=True)

# get character dictionary
src_word_dict = imdb_dataset.src_stoi
src_idx_dict = imdb_dataset.src_itos

SRC_PAD_IDX = src_word_dict['<PAD>']

# show sample reviews with pos/neg sentiments

show_sample_reviews = True

if show_sample_reviews:
    
    sample_text, sample_lab = next(iter(train_dataloader))
    slist=[]

    for stxt in sample_text[:4]: 
        slist.append([src_idx_dict[j] for j in stxt])

    for j, s in enumerate(slist):
        print('positive' if sample_lab[j]==1 else 'negative')
        print(' '.join([i for i in s if i != '<PAD>'])+'\n')


"""

model

"""

enc_vocab_size = len(src_word_dict) # counting eof, one-hot vector goes in

# Set hyperparam (model size)
# examples: model & ff dim - 8, 16, 32, 64, 128, numhead, numlayer 1~4

enc_d_model = 32

enc_d_ff = 128

enc_num_head = 4

enc_num_layer= 4

DROPOUT=0.1

model = sentiment_classifier(enc_input_size=enc_vocab_size,
                         enc_d_model = enc_d_model,     
                         enc_d_ff = enc_d_ff, 
                         enc_num_head = enc_num_head, 
                         enc_num_layer = enc_num_layer,
                         dropout=DROPOUT) 

model = model.to(dev)

"""

optimizer

"""

# Set hyperparam (learning rate)
# examples: 1e-3 ~ 1e-5

lr = 1e-3

optimizer = torch.optim.Adam(model.parameters(), lr = lr)

criterion = nn.BCEWithLogitsLoss()

"""

auxiliary functions

"""


# get length of reviews in batch
def get_lens_from_tensor(x):
    # lens (batch, t)
    lens = torch.ones_like(x).long()
    lens[x==SRC_PAD_IDX]=0
    return torch.sum(lens, dim=-1)

def get_binary_metrics(y_pred, y):
    # find number of TP, TN, FP, FN
    TP=sum(((y_pred == 1)&(y==1)).type(torch.int32))
    FP=sum(((y_pred == 1)&(y==0)).type(torch.int32))
    TN=sum(((y_pred == 0)&(y==0)).type(torch.int32))
    FN=sum(((y_pred == 0)&(y==1)).type(torch.int32))
    accy = (TP+TN)/(TP+FP+TN+FN)
            
    recall = TP/(TP+FN) if TP+FN!=0 else 0
    prec = TP/(TP+FP) if TP+FP!=0 else 0
    f1 = 2*recall*prec/(recall+prec) if recall+prec !=0 else 0
    
    return accy, recall, prec, f1

"""

train/validation

""" 


def train(model, dataloader, optimizer, criterion, clip):

    model.train()

    epoch_loss = 0

    for i, batch in enumerate(dataloader):

        src = batch[0].to(dev)
        trg = batch[1].float().to(dev)

        # print('batch trg.shape', trg.shape)
        # print('batch src.shape', src.shape)

        optimizer.zero_grad()

        x_lens = get_lens_from_tensor(src).to(dev)

        output = model(x=src, x_lens=x_lens) 


        output = output.contiguous().view(-1)
        trg = trg.contiguous().view(-1)
        
        loss = criterion(output, trg)

        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)

        optimizer.step()

        epoch_loss += loss.item()

    return epoch_loss / len(dataloader)

def evaluate(model, dataloader, criterion):

    model.eval()
    
    epoch_loss = 0
    
    epoch_accy =0
    epoch_recall =0
    epoch_prec =0
    epoch_f1 =0

    with torch.no_grad():
        for i, batch in enumerate(dataloader):

            src = batch[0].to(dev)
            trg = batch[1].float().to(dev)

            x_lens = get_lens_from_tensor(src).to(dev)

            output = model(x=src, x_lens=x_lens) 

            output = output.contiguous().view(-1)
            trg = trg.contiguous().view(-1)

            loss = criterion(output, trg)
            
            accy, recall, prec, f1 = get_binary_metrics((output>=0).long(), trg.long())
            epoch_accy += accy
            epoch_recall += recall
            epoch_prec += prec
            epoch_f1 += f1

            epoch_loss += loss.item()

    # show accuracy
    print(f'\tAccuracy: {epoch_accy/(len(dataloader)):.3f}')
    
    return epoch_loss / len(dataloader)

def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

"""

Training loop

"""

N_EPOCHS = 40
CLIP = 1

best_valid_loss = float('inf')

for epoch in range(N_EPOCHS):

    start_time = time.time()

    train_loss = train(model, train_dataloader, optimizer, criterion, CLIP)
    valid_loss = evaluate(model, val_dataloader, criterion)

    end_time = time.time()

    epoch_mins, epoch_secs = epoch_time(start_time, end_time)

    if valid_loss < best_valid_loss:
        best_valid_loss = valid_loss
        torch.save(model.state_dict(), 'model.pt')

    print(f'Epoch: {epoch+1:02} | Time: {epoch_mins}m {epoch_secs}s')
    print(f'\tTrain Loss: {train_loss:.3f} | Val. Loss: {valid_loss:.3f}')
        
"""

Test loop

"""
print('*** Now test phase begins! ***')
model.load_state_dict(torch.load('model.pt'))

test_loss = evaluate(model, test_dataloader, criterion)

print(f'| Test Loss: {test_loss:.3f}')
