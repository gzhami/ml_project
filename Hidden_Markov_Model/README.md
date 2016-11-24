## Hidden Markov Model Description

In this project, we performed part of speech tagging. The biggest challenge is that words are often obscure. For example, the 
word "fly" can be both a noun and a verb. We do not need to possess mastery of linguistics to solve this challenge; in fact, 
we are simply treat words as symbols and use Hidden Markov Model to ahiceve our goal. 

### Challenges
1. Underflow: when multiplying several probabilities together, the result can be very small. In fact, too small that many 
computer language will fail to represent it. Therefore, we might have a 0 return value when the true value is non-zero. To solve
this challenge, we will use logarithmic method to avoid the underflow problem. 

2. Time complexity: The time to compute the possibility of a sentence is O(n^k) where n is the number of symbols in the given
sequence and k is the number of states. This is not practical because it is too slow. However, we can resolve this problem using
dynamic programming to reduce the time complexity to O(nk^2). 

### Self Notes
1. Remember there are two important assumptions here. 
  1. Future state is independent of past states given current state. 
  2. Observations depend only on the current state. 
2. There are 3 acts in any HHM problems
  1. Evaluation: finding the probability of an observed sequence of symbols. 
  2. Decoding: finding the most likely state transition sequence. 
  3. Learning: adjusting parameters to maximize observed sequence probability. 



