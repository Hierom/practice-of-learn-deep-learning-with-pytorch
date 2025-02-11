from __future__ import print_function
import torch
from torch.autograd import Variable
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt

#  Define W and B
w_target = np.array([0.5, 3, 2.4])
b_target = np.array([0.9])

f_des = 'y = {:.2f} + {:.2f} * x + {:.2f} * x^2 + {:.2f} * x^3'.format(
    b_target[0], w_target[0], w_target[1], w_target[2])
print(f_des)

#  Plot
x_sample = np.arange(-3, 3.1, 0.1)
y_sample = b_target[0] + w_target[0] * x_sample + w_target[1] * x_sample**2 + w_target[2] * x_sample**3

plt.plot(x_sample, y_sample, label='real curve')
plt.legend()
plt.show()

#  Given data
x_train = np.stack(
    [x_sample**i for i in range(1, 4)], axis=1)  # x = [x, x^2, x^3]
x_train = torch.from_numpy(x_train).float()  # Transform Numpy to Tensor
y_train = torch.from_numpy(y_sample).float().unsqueeze(1)

#  Construct Linear Regression Model
w = Variable(torch.randn(3, 1), requires_grad=True)
b = Variable(torch.zeros(1), requires_grad=True)
x_train = Variable(x_train)  # Transform Tensor to Variable
y_train = Variable(y_train)


def multi_linear(x):
    return torch.mm(x, w) + b


#  Plotting before training
y_pred = multi_linear(x_train)

plt.plot(
    x_train.data.numpy()[:, 0],
    y_pred.data.numpy(),
    label='fitting curve',
    color='r')
plt.plot(x_train.data.numpy()[:, 0], y_sample, label='real curve', color='b')
plt.legend()
plt.show()


#  Loss
def get_loss(y_, y):
    return torch.mean((y_ - y_train)**2)


loss = get_loss(y_pred, y_train)
print(loss)

#  Auto gradient calculating with W & B by PyTorch
loss.backward()
print(w.grad)
print(b.grad)
#  Update one time in w, b
w.data = w.data - 0.001 * w.grad.data
b.data = b.data - 0.001 * b.grad.data
#  Result after update parameters
y_pred = multi_linear(x_train)

plt.plot(
    x_train.data.numpy()[:, 0],
    y_pred.data.numpy(),
    label='fitting curve',
    color='r')
plt.plot(x_train.data.numpy()[:, 0], y_sample, label='real curve', color='b')
plt.legend()
plt.show()

#  Updating 100 times for the parameters
for e in range(100):
    y_pred = multi_linear(x_train)
    loss = get_loss(y_pred, y_train)

    w.grad.data.zero_()
    b.grad.data.zero_()
    loss.backward()

    # Updating w & b
    w.data = w.data - 0.001 * w.grad.data
    b.data = b.data - 0.001 * b.grad.data
    if (e + 1) % 20 == 0:
        print('epoch {}, Loss: {:.5f}'.format(e + 1, loss.data[0]))

#  Result after update parameters in 100 times
y_pred = multi_linear(x_train)

plt.plot(
    x_train.data.numpy()[:, 0],
    y_pred.data.numpy(),
    label='fitting curve',
    color='r')
plt.plot(x_train.data.numpy()[:, 0], y_sample, label='real curve', color='b')
plt.legend()
plt.show()