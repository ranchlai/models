import paddle.nn.functional as F
from tqdm import tqdm
import numpy as np
import paddle
#loss_fn = paddle.nn.NLLLoss()
def test(epoch,test_loader,model,loss_fn,logger):
    
    model.eval()
    avg_loss_acc = np.zeros([2])

    bar = tqdm(total=len(test_loader))

    for batch_id, data in enumerate(test_loader()):
        xd, yd = data
        X = xd.unsqueeze((1))
        label = paddle.reshape(yd, [-1, 1])
        pred = model(X).squeeze()
        #pred = F.log_softmax(logits)
        avg_loss = loss_fn(pred, label)
        acc = np.mean(np.argmax(pred.numpy(),1)==label.numpy()[:,0])
        avg_loss_acc[0] = (avg_loss_acc[0]*batch_id + avg_loss.numpy()[0])/(1+batch_id)
        avg_loss_acc[1] = (avg_loss_acc[1] *batch_id + acc)/(1+batch_id)
        msg = 'epoch:{}, test loss:{:.2}'.format(epoch,avg_loss_acc[1])\
            + ', test acc:{:.2}'.format(avg_loss_acc[1])
        bar.set_description_str(msg)
        bar.update(1)        
       
    bar.close()
    logger.add_scalar(tag="test loss", step=epoch, value=avg_loss_acc[0])
    logger.add_scalar(tag="test acc", step=epoch, value=avg_loss_acc[1])
    return avg_loss_acc[1]
    

        
def evaluate(epoch,val_loader,model,loss_fn,logger):
    model.eval()
    avg_loss_acc = np.zeros([2])

    bar = tqdm(total=len(val_loader))

    for batch_id, data in enumerate(val_loader()):
        xd, yd = data
        X = xd.unsqueeze((1))
        label = paddle.reshape(yd, [-1, 1])
        pred = model(X).squeeze()
        #pred = F.log_softmax(logits)
        avg_loss = loss_fn(pred, label)
        
        acc = np.mean(np.argmax(pred.numpy(),1)==label.numpy()[:,0])
        avg_loss_acc[0] = (avg_loss_acc[0]*batch_id + avg_loss.numpy()[0])/(1+batch_id)
        avg_loss_acc[1] = (avg_loss_acc[1] *batch_id + acc)/(1+batch_id)
        msg = 'epoch:{}, val loss:{:.2}'.format(epoch,avg_loss_acc[0])\
            + ', val acc:{:.2}'.format(avg_loss_acc[1])
        bar.set_description_str(msg)
        bar.update(1)
    bar.close()
    logger.add_scalar(tag="eval loss", step=epoch, value=avg_loss_acc[0])
    logger.add_scalar(tag="eval acc", step=epoch, value=avg_loss_acc[1])
    return avg_loss_acc[1]
        
def train_one_epoch(epoch,train_loader,model,optimizer,loss_fn,logger):
    model.train()
    avg_loss_acc = np.zeros([2])

    bar = tqdm(total=len(train_loader))
    model.clear_gradients()
    for batch_id, data in enumerate(train_loader()):
        bar.update(1)
        xd, yd = data
        X = xd.unsqueeze((1))
        X.stop_gradient = False    
        yd.stop_gradient = False        
        
        label = paddle.reshape(yd, [-1, 1])
        pred = model(X).squeeze()
       # pred = F.softmax(logits)
        avg_loss = loss_fn(pred, label)
        
        acc = np.mean(np.argmax(pred.numpy(),1)==label.numpy()[:,0])
        avg_loss_acc[0] = (avg_loss_acc[0]*batch_id + avg_loss.numpy()[0])/(1+batch_id)
        avg_loss_acc[1] = (avg_loss_acc[1] *batch_id + acc)/(1+batch_id)
       # avg_loss_acc[2] += 1
        msg = 'epoch:'+ str(epoch)+ \
        ', batch:'+ str(batch_id)+ \
        ', train loss:{:.3}'.format(avg_loss_acc[0])\
        + ', train acc:{:.3}'.format(avg_loss_acc[1])
        #print(msg)
        
        #logger.log_str(msg,False)
        
        bar.set_description_str(msg)
        avg_loss.backward()
        optimizer.step()
        model.clear_gradients()
    bar.close()
    logger.add_scalar(tag="train loss", step=epoch, value=avg_loss_acc[0])
    logger.add_scalar(tag="train acc", step=epoch, value=avg_loss_acc[1])
    
        
