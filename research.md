---
layout: simple
title: Research
---


<style>
.hero-body .column {
	margin-bottom: 180px;
}

#email {
	text-align: center;
	font-size: 25px;
}
</style>

<script type="module">
// Forwards `subject` and `body` search params to the email link

const originalSearchParams = new URLSearchParams(location.search);
const element = document.querySelector('#email a');

const searchParams = new URLSearchParams();
if (originalSearchParams.has('subject')) {
	searchParams.set('subject', originalSearchParams.get('subject'));
}
if (originalSearchParams.has('body')) {
	searchParams.set('body', originalSearchParams.get('body'));
}

element.search = searchParams.toString();
</script>

# Research

Working Papers

---
<p style="text-align:justify"></p>
<p>
	<b>Tweeting for Money </b> with Javier Gil-Bazo (UPF and BGSE)


</p>

<p>
	<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3320606">Listening to the Fates: Investor Learning and the Likelihood of Future Events</a>

</p>

<p style="text-align:justify">Information that is difficult to quantify, process, and verify - commonly refered as qualitative
or soft information - is disclosed by firms, and processed by investors in financial markets. When
this information is informative, it affects investors’ decisions and moulds prices in equilibrium.
Despite its relevance, researchers lack a theoretical framework to model its impact on capital
allocation and its transmission by firms. I pretend to fill this gap by borrowing from the axiomatic decision making literature a framework to accomodate this information into expectation
formation. In particular I study how quantitative and qualitative information affect capital allocation in a market for mutual funds. In my model mutual fund investors learn about the ability
of a mutual fund manager to generate abnormal returns from past returns and a qualitative
signal. When investors observe past returns, they update their beliefs following Bayes rule, but
follow a more general rule consistent with rationality to accomodate the qualitative information
to their posterior. I study how this type of information affects capital allocation and disclosure.
Intuitively, investors seek funds with more favorable qualitative information. Due to its soft
nature, firms have incentives to manipulate the information. In equilibrium, reputation costs
decrease the probability of investors verifying information, and verification costs and investors’
risk aversion decrease the probability of funds manipulating information</p>
<b>Presentations: </b> ESADE (2018)

<p>
	<b> Joint Liquidity Management at Banks and Firms: 	A Structural Approach </b> with Filippo Ippolito (UPF and BGSE), Stefano Sacchetto (IESE), and Roberto Steri (University of Luxembourg)
</p>


---


