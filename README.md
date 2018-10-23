# Web front-end frameworks impact on energy consumption.

## Introduction




## Goal of the paper as defined based on the Goals, Questions and Metrics template(GQM): 

**_An analysis of front-end frameworks, for the purpose of evaluation in regards to their energy consumption, from the point of view of software developers, in the context of mobile development._**	


## Results


## Guidelines for experiment replication.


### Web front-end frameworks

Which libraries/frameworks are we comparing?
We included most of the implementations listed in the [RealWorld repo](https://github.com/gothinkster/realworld). Here we list them, sorted by popularity.

* [React/Redux](https://github.com/gothinkster/react-redux-realworld-example-app)
* [Angular](https://github.com/gothinkster/angular-realworld-example-app)
* [Vue](https://github.com/gothinkster/vue-realworld-example-app)
* [React/MobX](https://github.com/gothinkster/react-mobx-realworld-example-app)
* [AngularJS](https://github.com/gothinkster/angularjs-realworld-example-app)
* [Svelte/Sapper](https://github.com/sveltejs/realworld)
* [Angular + ngrx + nx](https://github.com/stefanoslig/angular-ngrx-nx-realworld-example-app)
* [ClojureScript + Keechma](https://github.com/gothinkster/clojurescript-keechma-realworld-example-app)
* [Dojo 2](https://github.com/gothinkster/dojo2-realworld-example-app)

Once all the repositories have been cloned, put all the folders inside a root folder. 

Please refer each links in order to install everything you need for run all the frameworks. Make sure to run only the commands for install the dependencies, without running the command for run the frameworks.

In order to start all the frameworks, open 9 different terminal windows and go to each sub-directories containing the repositories. Then run the following commands. 

* React/Redux: `npm start`
* Angular: `ng serve --host 0.0.0.0 --port 4201`
* Vue: `npm run dev`
* React/Mobx: `npm start`
* AngularJS: `gulp`
* Svelte/Sapper: `npm run dev`
* Angular + ngrx + nx: `ng serve --host 0.0.0.0`
* ClojureScript + Keechma: `lein figwheel dev`
* Dojo 2: `npm run dev`


### AndroidRunner

Once all the frameworks have been run, please go to the [AndoridRunner repository](https://github.com/S2-group/android-runner) and refer to the section "Install" in order to check all the techonologies you need. Then, in order to execute the experiment, clone this repository. Edit the "config.json" file modifying the "paths" field with the name of the framework which you execute the experiment.
<br />
Every execution of the experiment (one for each frameworks) is repeated 20 times with 2 minutes of interval between each repetition. This amount of time is introduced to be sure to not influence tentative each other. 
<br />
Then open a window terminal, go inside the root folder and run the fllowing command for every frameworks: `python2 android-runner android-runner/example/web/config.json`. Be sure that your device is connected to the laptop that you are using for the experiment.
<br />
The execution of each framework requires around 1 hour for all the 20 repetitions.

Note: Remember that the pc and the device need to be connected with the same network.

Note2: Remember to change the IP addresses inside the python adb file that we developed. The IP addresses must be changed inside the main function, in each objects that are using for open the frameworks.

Note3: If you have insalled both python3 and python2 and python3 is your current version, you may have problems with systrace. You could work around the problem creating a virtual environment for python. We used [Conda](https://conda.io/docs/). In the following [link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) a very useful guide for create a virtual environment for python with conda is explained. 

### RStudio
