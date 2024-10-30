# Run What?

## The premise
There are several meanings of the word 'run'. Same with American Sign Language. We sign 'run' in different ways according to what it actually means.

## The solution
I've recorded myself signing 'run' in different ways and uploaded it. GenAI will use embedding to decipher at what context does the word run means and tries to match it against a pre-defined dictionary. It'll spit out a URL that you can paste into your browser to see which sign for 'run' is it.

## Getting started locally
...

## Getting started with Docker
...

## Getting started on Kubernetes
Export your OPENAI_API_KEY this way (first, replace 'your_openai_api_key'):
```
$ kubectl create secret generic openai-secret --from-literal=OPENAI_API_KEY=your_openai_api_key
```

Install kind, create a cluster

