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

## Working Papers

---
<p style="text-align:justify"></p>

<p >
<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3711536">	<b>-  Stroke of a Pen: Investment and Stock Returns under  Energy Policy Uncertainty </b>  </a> (Job Market Paper)
</p>


<p style="text-align:justify; font-size:90%;"></p>

Presentations: UPF, Paris-Dauphine PSL, Bank of Lithuania, University of Bristol, University of Glasgow, CUNEF, Universitat de les Illes Balears 

<p>
	<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3719169"> <b>- Tweeting for money: Social media and mutual fund flows </b> </a> with <a href="https://www.javiergilbazo.es/">Javier Gil-Bazo (UPF and BGSE)</a>
</p>
<p style="text-align:justify; font-size:90%;"></p>

Presentations: French Finance Association, Spanish Finance Association, 
2022 Consortium on Asset Management and Fintech (Expected)


<p>
    <b> The forecasting power of short-term options </b> with <a> Arthur Böök</a> (ESADE), <a> Martin Reinke </a> (München), and <a href="https://www.esade.edu/faculty/carlo.sala"> Carlo Sala </a> (ESADE)
</p>

# Work in Progress

<p>
	<b> Joint Liquidity Management at Banks and Firms: 	A Structural Approach </b> with <a href="https://sites.google.com/site/filippoippolito/"> Filippo Ippolito</a> (UPF and BGSE), <a href="https://www.iese.edu/faculty-research/faculty/stefano-sacchetto/"> Stefano Sacchetto </a> (IESE), and <a href="https://sites.google.com/site/robertosteripersonalpage/"> Roberto Steri </a> (University of Luxembourg)
</p>

<p>
	<b> The rogue offshore finance industry: evidence from a structural estimation </b> with <a href="https://www.marceloortizm.com/"> Marcelo Ortiz</a> (UPF)
</p>


<!-- <p><a href="discussions/slides.pdf"> Download Slides</a></p> -->


---


