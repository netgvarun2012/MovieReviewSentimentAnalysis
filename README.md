# Movie Review Sentiment Analysis using LSTMs networks

## Introduction
This is a simple project to demonstrate the power of AI when dealing with sequential data. In particular, this falls under '**Sequence to Vector**' problem - We feed in a sequence of words (maybe a paragraph of movie review) and request back a vector indicating if its Positive or Negative review.

![image](https://user-images.githubusercontent.com/93938450/166919216-1a81c892-b9f5-4f95-ae1e-e7aeccd21cc2.png)

## Technologies used
LSTMs, Tensorflow, Python.

## Concepts

![image](https://user-images.githubusercontent.com/93938450/166941179-8ace3f56-9d63-4c87-91d5-2664706423f4.png)
![image](https://user-images.githubusercontent.com/93938450/166942183-af7d42a1-50a5-4fcf-9f41-bb5d5ddec59d.png)

- We have Forget gate first where we decide what information are we going to forget/throw away from the cell state ‘Ct-1’. 
- **Steps**: 
  Pass Ht-1 and Xt, then we perform linear weighted sum, then we pass it into a SIGMOID function!

  Output of SIGMOID function will be between 0 and 1 with :
  1- Keep it.
  0 - Forget it!



![image](https://user-images.githubusercontent.com/93938450/166940217-b169a11f-7b61-42ae-8551-d128b13b51ff.png)   

![image](https://user-images.githubusercontent.com/93938450/166940703-7912c949-e259-4558-856f-811c447b4d78.png)


