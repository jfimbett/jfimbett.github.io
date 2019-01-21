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
<p style="text-align:justify"><font size="-1"></font></p>

<p><a href="">Listening to the Fates: Investor Learning and the Likelihood of Future Events</a></p>

---


