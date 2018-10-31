# Gib Data
## Essentially like "Explore" on Google Sheets

*Gib Data* sorts and sifts past IB results. You might have wondered, in your
school: 

> * Do students generally do better in their HL classes compared to their SL 
classes? Are there trends in terms of taking more languages at HL vs. taking 
more math or science classes at HL?
> * Even though we don't have "filières" as they always have in the French 
Baccalaureate (S, L, ES...) are there trends in our students' subject choices 
that, in fact, show such a classification in IB students? 
> * Do students who score well on their TOK also score well in other 
essay-based subjects such as languages or history (and vice-versa, do science 
and math students score more poorly on TOK in general?)
> * Are there certain component results that don't fit the rest of the data?  
For example, do French B orals seem low compared to the other components such 
as the written task or the exam papers? 
> * Do students who do well on their EE also do equally as well in that 
subject?  Are there certain subjects where the EE results don't match the 
results for the rest of the class? 



## IMPORTANT NOTES ON PRIVACY
Below are Mr. Damon's words concerning the privacy policy that goes with this 
project:
> I would need full confidence in your ability to keep this data private. I 
have anonymized it, but still, there is enough information that you could guess 
some of the identities and for the subjects that only had 1 teacher last year, 
you would know which teacher the data is referring to.  The raw data as well as 
any information and  insights you gain from data mining would remain between us 
and should not be discussed with classmates and teachers and certainly should 
not be posted anywhere either inside or outside the school community.
> * The information in the data file is confidential.  Only the members of the 
club can view or access the information (any 'outside help' from friends would 
need to be checked with me first)
> * Any copies you have should be stored in such a way that they are secure and 
no one else can access them.  So, for example, keeping the data on a USB key 
that can be lost or stolen is out of the question. 
> * At the end of the project, the club's copy of the data should be deleted 
> * In addition to the data itself, any conclusions or trends found in the 
process of analyzing the data should remain confidential between me and the 
members of the club.  For example, if you find that Biology Extended Essays 
appear to score significantly lower than Physics and Chemistry EE's, we don't 
want you to go around telling everyone in 1ère not to do Biology for their EE.  
However, that information might help us identify an issue that needs to be 
addressed.  
> * No data or analysis should be posted on any kind of social media or web 
platform.  Any sharing between us needs to be by email only.  

## Useful Information
The raw data file `data/c2018.csv` is an ignored file for privacy reasons. By 
requesting access to last year's IB results, you agree to follow and adhere to 
the privacy policy stated above.

Here is some useful information concerning `data/c2018.csv`:

> * Registration number is the ID of the student whose name has been removed.  
This should be used as a key field and should not be deleted!
> * Component grade is out of 7 - a "component" is something a grade is awarded 
for such as a Paper 2, an IA, an oral, etc. 
> * Scaled total mark is out of 100 for most subjects.  It's basically 100%.  
Exceptions: TOK (out of 30) and the EE (out of 34). 
> * Be aware of the danger of analyzing small data sets.  If there are only 5 
or fewer students in a sample category you are analyzing, it's difficult to see 
any trends.
