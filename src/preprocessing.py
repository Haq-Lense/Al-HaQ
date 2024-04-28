from torch.utils.data import Dataset
import torch
import pandas as pd
from torch.nn.utils.rnn import pad_sequence

class FakeTweetsDataset(Dataset):
    def __init__(self, mode, tokenizer, path):

        assert mode in ['train', 'test']
        self.mode = mode

        self.df = pd.read_csv(path + '_'+mode + '.csv').fillna('')
        self.len = len(self.df)
        self.tokenizer = tokenizer

    def __getitem__(self, idx):

        tweet=self.df.iloc[idx]['statement']
        label=self.df.iloc[idx]['BinaryNumTarget']
        label_tensor = torch.tensor(label)

        word_pieces = ['[CLS]']
        tweet = self.tokenizer.tokenize(tweet)
        if len(tweet) > 100:
            tweet = tweet[:100]
        word_pieces += tweet + ['[SEP]']
        len_st = len(word_pieces)

        ids = self.tokenizer.convert_tokens_to_ids(word_pieces)
        tokens_tensor = torch.tensor(ids)

        segments_tensor = torch.tensor([0] * len_st, dtype=torch.long)

        return (tokens_tensor, segments_tensor, label_tensor)

    def __len__(self):

        print(self.df.groupby('label').size())
        return self.len


def create_mini_batch(samples):
    tokens_tensors = [s[0] for s in samples]
    segments_tensors = [s[1] for s in samples]

    if samples[0][2] is not None:

        label_ids = torch.stack([s[2] for s in samples])
    else:
        label_ids = None


    tokens_tensors = pad_sequence(tokens_tensors, batch_first=True)
    segments_tensors = pad_sequence(segments_tensors, batch_first=True)

    masks_tensors = torch.zeros(tokens_tensors.shape, dtype=torch.long)
    masks_tensors = masks_tensors.masked_fill(tokens_tensors != 0,1)

    return tokens_tensors, segments_tensors, masks_tensors, label_ids