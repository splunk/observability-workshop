---
title: Appendix - Setting up on Mac
linkTitle: Appendix - Mac Setup
weight: 99
---

## Mac Setup

* Tested on
  * Macos Ventura 13.2.1
  * Mac M1/M2

Intel Macs should be work; however if they are slower you may need to run `./BuildAndDeploy` multiple times.

IMPORTANT: Docker must have access to 6-GB RAM.

* Prerequisites
  * [XCode Command line tools](https://mac.install.guide/commandlinetools/index.html)

### Homebrew Install

* [Homebrew full install details](https://docs.brew.sh/Installation)

``` bash
mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew
eval "$(homebrew/bin/brew shellenv)"
brew update --force --quiet
chmod -R go-w "$(brew --prefix)/share/zsh"
```

#### Install Colima

Colima - Colima is a docker daemon that does not require Docker Desktop. This is used to avoid any docker license issues with Docker Desktop.

* [Colima full install details](https://github.com/abiosoft/colima)

``` bash
brew uninstall docker docker-compose colima
brew install docker docker-compose colima 
colima stop
colima start --cpu 4 --memory 6
```

* Java Tools Install

``` bash
brew install git
brew install maven
```
