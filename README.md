# PyEuchre
For generating statistics and probabilities for Euchre games/tricks.




goal: to be able to determine which card should be played on any given trick (knowing or not knowing your partner's hand) as well as determine when to call, what suit to call, etc (perhaps 2 separate things)

call the first Trick Stage

TrickStage(object):
A given player would have a variable amount of knowledge: of cards in their hand or in others, or discarded
given this information, the object has to solve() returning the likelihood of winning the trick and the hand, listing the cards by hand expected value
