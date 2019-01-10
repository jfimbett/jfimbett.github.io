---
layout: simple
title: Contact
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

# Notes

In this page I present posts about things that I have struggled with during my research, and to avoid reinventing the wheel have decided to post solutions. All comments are welcome

---

# Estimating and testing a linear aset pricing model via GMM

---

Cochrane 2005 writes some example...
<figure>
  <figcaption>Your code title</figcaption>
  <pre>
    <code contenteditable spellcheck="false">
      <!-- your code here -->
      some_code
    </code>
  </pre>
</figure>
