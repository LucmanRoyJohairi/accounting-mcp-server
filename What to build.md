What to build

Three parts, in this order.
A local MCP server over the dataset. It gives Claude tools to read invoices, look up prices and work orders, and look up contract rules. Keep the tools small and clearly named.
A Claude skill that uses those tools to check every invoice and give Consultee a review list. For each problem: the invoice, the line, the contract rule it breaks, the amount to dispute, and the evidence. For each invoice: a proposed verdict of approve, dispute or hold, for Consultee to decide on.
The run. Run it on all 40 invoices, with a total of what Oostervelde should dispute. Then compare the first 10 with Consultee's verdicts and explain every difference. Don't assume she's always right.
Consultee stays in charge

Where does a person decide?
That part of the design is yours.

Consultee signs off on every payment, and she won't approve 40 invoices on a computer's word. Your solution has to keep her in the loop. How you do that is up to you. Some questions you'll need to answer for yourself:

Which calls can your solution make on its own, and which should always go to Consultee?
What does she see when your solution isn't sure, and how does she say yes, no or change this?
Can anything reach a contractor without her approval?
When she overrules your solution, what happens with that?
There's no single right answer. We look at whether your choices fit Consultee and her work, and whether you can explain them. Show it in your video and explain it in your NOTES.md.


Your code. The MCP server and the skill, with a README we can follow to run it ourselves in 10 minutes.
The review list for all 40 invoices, exactly as your skill produced it.
Your comparison with Consultee's 10 verdicts, with every difference explained.
NOTES.md, with four headings:
Decisions and translations. Every place where the contract or the data left room for interpretation, what you chose and why, and the translations you relied on.
Where Consultee decides. What your solution does on its own, what goes to her, and why.
What changed along the way. Building a skill is trial and error. Which approaches didn't work, what you noticed, and what you changed because of it.
What isn't finished. What's missing, and what you would do next.
A video of 5 minutes at most, on your own screen and in your own voice. The skill running, one hard case explained, and one thing your solution still gets wrong.