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
<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3711536">	<b>-  Stroke of a Pen: Investment and Stock Returns under  Energy Policy Uncertainty </b>  </a>
</p>
<p>
    Job Market Paper
</p>

<p style="text-align:justify; font-size:90%;"></p>

Presentations: UPF, Paris-Dauphine PSL, Bank of Lithuania, University of Bristol, University of Glasgow, CUNEF, Universitat de les Illes Balears 

<p>
	<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3719169"> <b>- Tweeting for money: Social media and mutual fund flows </b> </a> with <a href="https://www.javiergilbazo.es/">Javier Gil-Bazo (UPF and BGSE)</a>
</p>


<p>
<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3320606">	<b>-  Learning from Quant (Qual)-itative Information </b> </a>
</p>

<b>Presentations: </b> ESADE (2018)

<a href="assets/online_appendices/frl_onlineappendix.pdf"> Online Appendix </a>

## Work in Progress
<p>
	<b> Joint Liquidity Management at Banks and Firms: 	A Structural Approach </b> with <a href="https://sites.google.com/site/filippoippolito/"> Filippo Ippolito</a> (UPF and BGSE), <a href="https://www.iese.edu/faculty-research/faculty/stefano-sacchetto/"> Stefano Sacchetto </a> (IESE), and <a href="https://sites.google.com/site/robertosteripersonalpage/"> Roberto Steri </a> (University of Luxembourg)
</p>

<p>
    <b> The forecasting power of short-term options </b> with <a> Arthur Böök</a> (ESADE), <a> Martin Reinke </a> (München), and <a href="https://www.esade.edu/faculty/carlo.sala"> Carlo Sala </a> (ESADE)
</p>

# Discussions

What drives Q and investment Fluctuations?
Illan Cooper, Paulo Maio, and Chunyu Yang
2nd Corporate Policies and Asset Prices Conference
Cass Business School, London
December 2018
<i> Slides upon request </i>
<!-- <p><a href="discussions/slides.pdf"> Download Slides</a></p> -->


---


