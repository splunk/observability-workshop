# streaming-analytics-workshop
Files used for creation of workshop instances, useful tools and anything else!

Install Multipass for your OS - https://multipass.run/. On a Mac you can also install via brew e.g. `brew cask install multipass`

Launch the Multipass instance which will run Kubernetes e.g.

```
multipass launch --name k3s --cloud-init cloud-init-k3s.yaml --cpus=2 --mem=2G
```
