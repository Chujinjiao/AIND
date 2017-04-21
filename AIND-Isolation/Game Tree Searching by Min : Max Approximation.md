## Game Tree Searching by Min / Max Approximation

### Techniques introduced

This paper try to introdeces a new technique for searching in game tree, based on the idea of approximating the min and max operators with generalized mean-value operators.

The key part is **Generalised Mean Values** (use gmv for short for the rest)

Let  **a** be a vector of **n** positive real number and _p_ be a nonzero real number, define the generalized p-mean of **a**:
$$
M_p(a)=({\frac{1}{n}} \sum_i^n a_i^p)^ {\frac{1}{p}}
$$
as _p_ goes to infinity,  this equation give us those two number:


$$
\lim_{p \to \infty} M_p(a) = \max(a_1, ...,a_n)
$$
and
$$
\lim_{p \to -\infty} M_p(a) = \min(a_1, ...,a_n)
$$
For large positive or negative values of _p_, gmv is a good approximation to max(a) or min(a), respectively.  Another intheresting part is gmv's derivatives with respect to each variable a is *continuous*.

By using the gmv values to approximate the min and max functions, we can identify in an interesting way that leaf in a game tree upon whose value the value at the root depends most strongly(by taking derivatives). This leaf will be the one to expand next.



### Results

The Generalised Mean Values approach can produce play superior to taht produced by minimax search with alpha-beta pruning, based on the same number of calls to the underlying 'move' operator. But under limiting CPU time resource condition gmv not as good as minimax, due to computational difficulty.