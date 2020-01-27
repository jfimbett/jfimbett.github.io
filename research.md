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
	<b>Expected Returns and Political Agenda Uncertainty </b> 
</p>
<p style="text-align:justify">Political Uncertainty is inversely related to how well an economic agent can forecast political decisions. Using data on the US political agenda and a data rich forecasting exercise, I develop a multi-dimensional index of political uncertainty that isolates its source (executive or legislative) and content of the political decisions from which the uncertainty arises. Guided by restrictions on potential state-variables consistent with the ICAPM and large statistical thresholds, I study the relation between political uncertainty and financial markets. Executive political uncertainty, arising from blurriness in forecasting executive order decisions related to Energy and Immigration by the US President, negatively captures aggregate market expected excess return variation. Moreover, innovations on these uncertainty measures are priced in the cross-section of expected returns.</p>


<p>
	<b>Listening to the Fates: Investor Learning and the Likelihood of Future Events</b>

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

<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3320606"> Download Paper </a>

<p>
	<b> Joint Liquidity Management at Banks and Firms: 	A Structural Approach </b> with Filippo Ippolito (UPF and BGSE), Stefano Sacchetto (IESE), and Roberto Steri (University of Luxembourg)
</p>

# Discussions

What drives Q and investment Fluctuations?
Illan Cooper, Paulo Maio, and Chunyu Yang
2nd Corporate Policies and Asset Prices Conference
Cass Business School, London
December 2018
<a href="discussions/slides.pdf"> Download</a>

---


