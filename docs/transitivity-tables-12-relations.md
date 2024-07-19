

![](https://cdn.mathpix.com/snip/images/KNcc_ZYU16fkx0rNGLkg-wTX3ZtbGbAs26HzDGPXwDw.original.fullsize.png)

<!-- 
| Name | Definition |
| :--- | :--- |
| before | $b(A, B) \equiv a^{+}<b^{-}$ |
| overlaps | $o(A, B) \equiv a^{-}<b^{-}$and $b^{-}<a^{+}$and $a^{+}<b^{+}$ |
| during | $d(A, B) \equiv b^{-}<a^{-}$and $a^{+}<b^{+}$ |
| meets | $m(A, B) \equiv a^{+}=b^{-}$ |
| starts | $s(A, B) \equiv a^{-}=b^{-}$and $a^{+}<b^{+}$ |
| finishes | $f(A, B) \equiv a^{+}=b^{+}$and $b^{-}<a^{-}$ |
| equals | $e(A, B) \equiv a^{-}=b^{-}$and $a^{+}=b^{+}$ |
| after | $b i(A, B) \equiv b(B, A)$ |
| overlapped-by | $o i(A, B) \equiv o(B, A)$ |
| contains | $d i(A, B) \equiv d(B, A)$ |
| met-by | $m i(A, B) \equiv m(B, A)$ |
| started-by | $s i(A, B) \equiv s(B, A)$ |
| finished-by | $f i(A, B) \equiv f(B, A)$ |
-->


> [!NOTE]
> *see: https://cedric.cnam.fr/~hamdif/upload/DEXA19/Transitivity_Tables.pdf*

| R1(P, I) | Before(P, I) | After(P, I) | Starts(P, I) | During(P, I) | Ends(P, I) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Before(I, L) | Before(P, L) | One of the <br> time point <br> relations | Before(P, L) | Before(P, L) | Before(P, L) |
| After(I, L) | One of the <br> time point <br> relations | After(P, L) | After(P, L) | After(P, L) | After(P, L) |
| Started-by(I, L) | Before(P, L) | After(P, L) | Equals(P, L) | After(P, L) | After(P, L) |
| Contains(I, L) | Before(P, L) | After(P, L) | Before(P, L) | One of the <br> time point <br> relations | After(P, L) |
| Ended-by(I, L) | Before(P, L) | After(P, L) | Before(P, L) | Before(P, L) | Equals(P, L) |


![](https://cdn.mathpix.com/snip/images/KXVa-ms7mQZ_OBLZVIrX_-ZVACWC_uGXg9SW8QDFjec.original.fullsize.png)


Maintaining Knowledge
about Temporal
Intervals
JAMES F. ALLEN The University of Rochester 


### Maintaining knowledge about temporal intervals
Item Type 	Journal Article

#### Abstract 	
An interval-based temporal logic is introduced, together with a computationally effective reasoning algorithm based on constraint propagation. This system is notable in offering a delicate balance between expressive power and the efficiency of its deductive engine. A notion of reference intervals is introduced which captu~s the temporal hierarchy implicit in many domains, and which can be used to precisely control the amount of deduction performed automatically by the system. Examples are provided for a database containing historical data, a database used for modeling processes and proce~ interaction, and a database for an interactive system where the present moment is continually being updated.

```
URL 	https://dl.acm.org/doi/10.1145/182.358434
Volume 	26
Pages 	832-843
Publication 	Communications of the ACM
DOI 	10.1145/182.358434
Issue 	11
Journal Abbr 	Commun. ACM
ISSN 	0001-0782, 1557-7317
```
Date Added 	7/19/2024, 3:37:21 AM
Modified 	7/19/2024, 3:37:21 AM
