import torch.nn as nn
import torch
import math
from torchtext.vocab import GloVe
from torchtext.data.utils import get_tokenizer
def setup():
   glove_embedding = GloVe(name='6B',dim=100)
   tokenizer = get_tokenizer('basic_english')
   vocab = torch.load("vocab/spam_not_spam_vocab.pth",map_location=torch.device('cpu'))
   return glove_embedding,tokenizer,vocab
class PositionalEncoding(nn.Module):
    def __init__(self,d_model,seq_len):
        super().__init__()
        self.dropout = nn.Dropout(0.1)
        pe = torch.zeros(seq_len,d_model)
        positions = torch.arange(0,seq_len,dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0,d_model,2).float() * (-math.log(10000)/d_model)
        )
        pe[:,0::2] = torch.sin(positions * div_term)
        pe[:,1::2] = torch.cos(positions * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe",pe)

    def forward(self,x):
       x = x + self.pe[:,:x.size(1),:]
       return self.dropout(x)

class EncoderTransformer(nn.Module):
  def __init__(self,glove_embedding,vocab):
    super().__init__()
    self.emb = nn.Embedding.from_pretrained(glove_embedding.vectors,freeze=True)
    self.encoder_layer = nn.TransformerEncoderLayer(d_model=self.emb.embedding_dim,nhead=10,dim_feedforward=100,dropout=0.1)
    self.encoder = nn.TransformerEncoder(self.encoder_layer,num_layers=6)
    self.pos_encoding = PositionalEncoding(self.emb.embedding_dim,len(vocab))
    self.linear = nn.Linear(self.emb.embedding_dim,2)
  def forward(self,x):
    x = self.emb(x) * math.sqrt(self.emb.embedding_dim)
    x = self.pos_encoding(x)
    x = self.encoder(x)
    x = x.mean(dim=1)
    x = self.linear(x)
    return x

def load_model(glove_embedding,vocab):
   transformer = EncoderTransformer(glove_embedding,vocab)
   transformer.state_dict = torch.load('models/spam_not_spam_model.pth',map_location=torch.device('cpu'))
   return transformer
def classify(inp:str,vocab,tokenizer,transformer):
   inp = torch.tensor(vocab(tokenizer(inp)),dtype=torch.long).unsqueeze(0).to(torch.device('cpu'))
   out = transformer(inp)
   out = torch.max(out.data,1)[1]
   if out == torch.tensor(0):
      return "not_spam"
   else:
      return "spam"
