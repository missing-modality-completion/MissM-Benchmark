import torch
from torch.utils.data import DataLoader
import pickle


class MMDataset_sims(torch.utils.data.Dataset):
    def __init__(self, data, missing=False, missing_index=None):
        self.data = data
        self.missing = missing
        self.missing_index = missing_index if missing else [0 for _ in range(len(data['label']))]

    def __len__(self):
        return len(self.data['label'])

    def __getitem__(self, index):
        data = {
            'language': torch.tensor(self.data['language'][index]),
            'video': torch.tensor(self.data['video'][index]),
            'audio': torch.tensor(self.data['audio'][index])
        }
        label = {
            'label': self.data['label'][index],
            'label_T': self.data['label_T'][index],
            'label_A': self.data['label_A'][index],
            'label_V': self.data['label_V'][index],
            'annotation': self.data['annotation'][index]
        }

        return data, label, self.missing_index[index]


def data_loader(batch_size, dataset, missing=False, missing_type='language', missing_ratio=0.3):
    if dataset == 'sims':
        embedding_path = '/big-data/person/yuanjiang/MLMM_datasets/CH-SIMS/embedding.pkl'
        with open(embedding_path, 'rb') as f:
            data = pickle.load(f)

        missing_index = None
        if missing:
            with open("/".join(embedding_path.split("/")[:-1]) + "/" + "missing_index.pkl", 'rb') as f:
                missing_index = pickle.load(f)[missing_type][missing_ratio]

        train_data = MMDataset_sims(data['train'], missing, missing_index)
        test_data = MMDataset_sims(data['test'])
        val_data = MMDataset_sims(data['valid'])
        train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)
        val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader, val_loader


if __name__ == '__main__':
    train_loader, _, _ = data_loader(batch_size=2, dataset='sims')
    for data, label in train_loader:
        print(data['language'].shape)
        print(label)
        break
