# Web front-end frameworks impact on energy consumption

## Introduction

In   the   modern   age   of   information   and   communication systems,  traditional  desktop  applications  have  moved  to  the cloud. The need for applications to be cross-platform and offer mobile  device  support,  has  gotten  the  user  interface  to  lie  inits  entirety  through  the  window  of  a  web  browser.

This rapid  growth  and  expansion  of  mobile  devices  has  pushed software developers to explore, evaluate and experiment with several  web  front-end  frameworks  necessary  for  mobile  web application development. During  the  recent  years,  an  abundance  of  front-end  web development  frameworks  have  been  introduced  to  the  market, as an answer to the tedious process of having to tweak the web application front-end to  also have  the  desired  look  on  mobile. Apart  from  the  look  and  feel,  developers  want  to  know which web front-end frameworks are optimized and offer great performance. Developers are constantly looking for web front-end frameworks that consume less battery in users' devices. As   mobile   software   applications   operate   in   resource-constrained environments, guidelines to build energy efficient applications  are  of  utmost  importance.

The  aim  of  our experiment  is  to  evaluate  the  energy  consumption  of  each framework,  using  different  measurements  that  will  be  taken when  an  Android  device  is  running  a  web  application.  The results  could  reveal  the  frameworks  with  the  highest  energy consumption, granting developers additional guidance for taking informed decisions regarding this matter. The focus of our experiment will be on a project called "RealWorld" created by Eric Simons. Each implementation of this project uses the same HTML structure, CSS, and API specifications, but a different library/framework.


## Guidelines for experiment replication


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

Please refer each links in order to install everything you need to run all the frameworks. Make sure to run only the commands for installing the dependencies, without running the command to run the frameworks.

Before starting all the frameworks, just a little modification is needed. Go the React/Mobx folder and open the package.json file. In the section "script" and in the option "start" add the following code: `PORT=3006` before "react-scripts start".

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

Once all the frameworks have been run, please go to the [AndroidRunner repository](https://github.com/S2-group/android-runner) and refer to the section "Install" in order to check all the techonologies you need. Then, in order to execute the experiment, clone this repository. Edit the "config.json" file modifying the "paths" field with the name of the framework with which you execute the experiment. Additionally, you have to decomment the relative two lines of codes inside the "adb.py" file relative to the framework you are executing (in the main function). You can find these two files inside the folder android-runner/example/web.
<br />
For example, if you are running the AngularJS framework, you may modify the "config.json" file, by adding "AngularJS" as the path and decomment the following lines of code inside the "adb.py" file:
`#angularJS = Scenario("http://192.168.43.164:4000", 1105, 327, 621, 579, 621, 704, 924, 776, 968, 324, 403, 436, 525, 1139, 457, 1330, 599)`
<br />
`#angularJS.processUrl()`
<br />
You have also to modify the monkeyrunner_path, adb_path, systrace_path and powerprofile_path inside the config.json file. 
<br />
Every execution of the experiment (one for each frameworks) is repeated 20 times with 2 minutes of interval between each repetition. This amount of time is introduced to be sure to not influence tentative each other. 
<br />
Then, open a window terminal, go inside the root folder and run the following command for every frameworks: `python2 android-runner android-runner/example/web/config.json`. Be sure that your device is connected to the laptop that you are using for the experiment.
<br />
The execution of each framework requires around 1 hour for all the 20 repetitions.

For having a more clear folder with all the results (output folder), we edited by hand the names of the folders. Every time that a test has been performed we edited the name of the output folder adding "_nameframework" ath the end. This has been done just for have a more readble folder.

*Note: Remember that the pc and the device need to be connected in the same network.*

*Note2: Remember to change the IP addresses inside the python adb file that we developed. The IP addresses must be changed inside the main function, in relation to the objects that you are using for open the frameworks.*

*Note3: If you have installed both python3 and python2 and python3 is your current version, you may have problems with systrace. You could work around the problem creating a virtual environment for python. We used [Conda](https://conda.io/docs/). In the following [link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/) a very useful guide for create a virtual environment for python with conda is explained.*

### Statistical Analysis

For the statistical analysis and the hypotheses testing, we used the R statistical language and moreover, the RStudio which is an IDE for R. 
In order to reproduce our analysis and get the expected results, a few steps must be done priorly.

The first step is to is to create a folder named "Aggregated_Results" inside the directory of the RScripts/RProject.

In this directory you need to place all the "aggregated_results.csv" files from the experiments you conducted, using Android-Runner.

Afterwards, you need to run the DataExploration.R script which will aggregate all data from the csv files you placed beforehand in the  "Aggregated_Results" directory into one large csv, namely "aggregated_data.csv" in the outer directory.

Then, from the same directory as "aggregated_data.csv" you have to run the DataAnalysis.R script which will conduct our main analysis and hypotheses testing. Moreover, it will load the data, plot them and run the actual hypotheses tests as mentioned in the paper.

*Note: In order to run the DataAnalysis.R script you need to make sure that you have the required packages, namely ggplot for plotting the graphs, car for the Levene homogeneity of variance test, Reshape for data reshaping and sjstats for common statistical computations.*
