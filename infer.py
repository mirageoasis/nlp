import torch
from pytorch_lightning import LightningModule, Trainer, seed_everything
import trainning

# loop = True;

# while loop: 
#   sentence = input("하고싶은 말을 입력해주세요 : ") 
#   if sentence == 0: 
#     break;
#   print(infer(sentence))


MODEL_PATH = "./lightning_logs/version_2/checkpoints/*.ckpt"
#HPARAMS_PATH = "./lightning_logs/version_2/hparams.yaml"

from glob import glob

LABEL_COLUMNS=["욕설","모욕","폭력위협/범죄조장","외설","성혐오","연령","인종/출신지","장애","종교","정치성향","직업혐오"]

latest_ckpt = sorted(glob(MODEL_PATH))[0]
#model = trainning.Model.load_from_checkpoint(latest_ckpt, hparams_file=HPARAMS_PATH)
model = trainning.Model.load_from_checkpoint(latest_ckpt)

model.eval()
#map location 해주면 환경 바뀌어도 가능
def main():
    #checkpoint = torch.load(MODEL_PATH)
    #print(model["hyper_parameters"])
    while True:
        sentence = input("문장을 입력하시오! ")
        judge(sentence=sentence)
    
def infer(x):
    return model(**model.tokenizer(x, return_tensors='pt'))
    
def judge(sentence):
    if sentence == "":
        print("빈 문장")
    else:
        _, test_prediction = infer(sentence)
        #print(type(test_prediction))
        #print(test_prediction)
        test_prediction = test_prediction.detach().flatten().numpy()
        for i in zip(LABEL_COLUMNS, test_prediction):
            # if i[1] > 0.5:
            # print(f'{i:.2f}')
            print(f'{i[0]} : {i[1]:.4f}')
            #print(f'probability : {prediction}')
        while True:
            sentence = input("문장을 입력하시오 : ")
            judge(sentence)

if __name__ == "__main__":
    main()