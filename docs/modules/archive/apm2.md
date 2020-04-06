# µAPM Workshop on K8S

In this module we will instrument a Node.js and a Python application that run on Kubernetes.

## Step 1: Explore the sample Node.js app

We are using a slightly modified version of [knote][] from a [Node.js on K8S Tutorial][]. It is located in the `apm/js` directory. The app itself is in `app/index.js`. It also has configuration for running on kubernetes in the folder `k8s` and a `Dockerfile` for building the image.

## Step 2: Instrument the Node.js app

The app is instrumented as per our [Node.js instrumentation guide][]:

1. `Dockerfile` installs the required package dependency as part of the docker image build:

    ```bash
    npm i -S signalfx-tracing
    ```

2. Sets up the OpenTracing instrumentation in `app/index.js` before requiring any other packages:

    ```javascript
    const tracer = require('signalfx-tracing').init({
      service: process.env.SIGNALFX_SERVICE_NAME || 'knote-js',
      url: `${process.env.SIGNALFX_AGENT_HOST}:9080/v1/trace`
    })
    ```
    
3. Review the K8S configuration in `k8s/knote.yaml` and observe the environment variables used in `index.js` are set there.

[Node.js instrumentation guide]: https://github.com/signalfx/signalfx-nodejs-tracing#usage
[knote]: https://github.com/learnk8s/knote-js/tree/master/04-05
[Node.js on K8S Tutorial]: https://learnk8s.io/nodejs-kubernetes-guide

## Step 3: Build the Docker image for the Node.js app

The workshop multipass instance comes with a local docker registry running on `registry.local:5000`. Docker is pre-configured to obtain images from this registry.

1. Let's build the images for our app:

	```bash
	docker build . -t registry.local:5000/knote-js:3.0.0
	```

2. Then transfer them to the registry with:

	```bash
	docker push registry.local:5000/knote-js:3.0.0
	```

## Step 4: Deploy the Node.js app on K8S

1. From the `workshop/apm/js` directory, review  from `k8s/knote.yaml` again and replace `[INITIALS]` with your actual initials.

2. Then apply the configuration:

	```bash
	kubectl apply -f k8s
	```

   Observe as pods are being created:

	```bash
	kubectl get pods -l app=knote --watch
	```

3. When this shows a running pod for knote, interrupt with `Ctrl-C` and obtain the service ip:

	```bash
	IP=$(kc get svc knote -o jsonpath='{.spec.clusterIP}')
	echo $IP
	```

4. Validate that the app is running:

	```bash
	curl -L http://$IP/
	```

	It should serve some HTML markup similar to:

	```html
	<html><head><title></title><link rel="stylesheet" href="tachyons.min.css"/></head><body class="ph3 pt0 pb4 mw7 center sans-serif"><h1 class="f2 mb0"><span class="gold">k</span>note</h1><p class="f5 mt1 mb4 lh-copy">A simple note-taking app.</p><form action="/note" method="POST" enctype="multipart/form-data"><ol class="list pl0"><li class="mv3"><label class="f6 b db mb2" for="image">Upload an image</label><input class="f6 link dim br1 ba b--black-20 ph3 pv2 mb2 dib black bg-white pointer" type="file" name="image"/><input class="f6 link dim br1 ba bw1 ph3 pv2 mb2 dib black bg-white pointer ml2" type="submit" value="Upload" name="upload"/></li><li class="mv3"><label class="f6 b db mb2" for="description">Write your content here</label><textarea class="f4 db border-box hover-black w-100 measure ba b--black-20 pa2 br2 mb2" rows="5" name="description"></textarea><input class="f6 link dim br1 ba bw1 ph3 pv2 mb2 dib black bg-white pointer" type="submit" value="Publish" name="publish"/></li></ol></form><p class="lh-copy f6">You don't have any notes yet.</p></body></html>
	```

## Step 5: Test the running Node.js app 

1. This is a simple note taking app, so let's make some notes by adding random words:

	```bash
	for i in {1..10}; do curl -L -F"image=" -F"description=$(shuf -n1 /usr/share/dict/words)" http://$IP/note; done
	```

2. If you curl the app again you should now see a list of notes after the above markup:

	```html
	…
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>semiretired</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>streakier</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>relay&#39;s</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>seconding</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>rouged</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>pours</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>disproof</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>exhortation</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>sprigs</p>
	</p></li><li class="mv3 bb bw2 b--light-yellow bg-washed-yellow ph4 pv2"><p class="measure"><p>tramped</p>
	```

3. Let's simulate load for the app:

	```bash
	ab -n 1000 -c 20 http://$IP/
	```

At this point you should see traffic in your µAPM view. 

## Step 6: Explore the sample python app

## Step 7: Instrument the python app

## Step 8: Build the Docker image for the Python app

## Step 9: Deploy the Python app on K8S

## Step 10: Test the running Python app


