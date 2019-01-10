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
    <code>
      <!-- your code here -->
g_all <- function (parms,X) {
 a <- parms[1:25]
 b <- parms[26:50]
 s <- parms[51:75]
 h <- parms[76:100]
 lambda_market<-parms[101]
 lambda_smb<-parms[102]
 lambda_hml<-parms[103]
 mktrf<-X[,26]
 smb<-X[,27]
 hml<-X[,28]
 mcond<-c()
 for (i in 1:25){ 
   e <- X[,i]- a[i]- b[i]*mktrf-s[i]*smb-h[i]*hml
   mcond <- cbind(mcond,e,e*mktrf, e*smb, e*hml)
 }
			  
 for (i in 1:25){ 
   e <- X[,i]- b[i]*lambda_market-s[i]*lambda_smb-h[i]*lambda_hml
   mcond <- cbind(mcond,e)
 }
 return (mcond);
}
    </code>
  </pre>
</figure>
<xmp>

</xmp>
