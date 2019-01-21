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

<p>
	<a href="">Tweeting for Money </a> (with Javier Gil-Bazo)
</p>

<p><b >Abstract</b></p>
<p style="text-align:justify">Information disclosure is crucial for the well-functioning of financial markets. Regulators determine what information, at which frequency, and in which format firms must disclose to investors. However, firms can choose to communicate directly with current and potential investors. While such direct communication is not always observable to the researcher, social media posts are public and therefore provide a unique opportunity to study non-mandatory information disclosure. Using machine learning algorithms and a database of almost 1 million posts by fund families in Twitter between 2009 and 2015, we study the determinants of voluntary information disclosure, its influence on investors' decisions, and the informativeness of its contents with respect to future fund performance. We find that larger, younger, and less complex fund families tweet more. Investors react to the possitiveness of tweets that fund families post. A one standard deviation increase in the positiveness of tweets increases fund inflows by 1.2 percent per year, or 6 million dollars per year for the average fund.  However, our results also suggest that disclosures are uninformative with respect to future fund performance. We find some mixed evidence suggesting that unsophisticated investors react more to this information despite its non-informative nature</p>

<p><a href="">Listening to the Fates: Investor Learning and the Likelihood of Future Events</a></p>

---


