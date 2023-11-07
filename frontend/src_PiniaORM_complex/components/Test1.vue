<template>

    <button type="button" @click="setData">Create</button><br>

    <button type="button" @click="getData">Request</button><br>
    <br><h3>Results</h3>
    <div v-for="record of display.results" >
      {{record}}
    </div>

</template>

<script>
import {usePerson, usePersonProjectStatus, useProject, 
  useEvent, useFeedback, useLifecycle, 
  useLifecycleStep, useAccount
} from '@/main.js';
import {populateAccountTestData,
  defaultLifecycle, defaultSteps,
  populateProjectTestData, populateContactTestData,
  populateEventTestData, populateFeedbackTestData
} from '@/assets/defaults.js'

export default {
  name: `Test`,
  data() {
    return {
      display:{
        results:[]
      }
    }
  },
  methods:{
    setData(){
      save_lifecycle()
      save_project()
      save_persons()
      save_event()
      save_feedbacks()
      
    },
    getData(){
      /*
      const lifecycles = get_lifecycles()
      this.display.results.length = 0
      this.display.results.push(...lifecycles )

      const lifecycles = get_lifecycles_with_projects()
      this.display.results.length = 0
      this.display.results.push(...lifecycles )
      
      const projects = get_projects()
      this.display.results.length = 0
      this.display.results.push(...projects )
      
      const persons = get_persons_with_nested_status()
      this.display.results.length = 0
      this.display.results.push(...persons )
      
      const events = get_events()
      this.display.results.length = 0
      this.display.results.push(...events )
      */
      const feedbacks = get_feedbacks()
      this.display.results.length = 0
      this.display.results.push(...feedbacks )
    }
  }
};

/*
## Insert (Save / Update)

* New Lifecycle - tables: Lifecycle > LifecycleStep
* New Project - tables: Project > Lifecycle
* New Contact - tables: Person > Project(s) > PersonProjectStatus > Person (ReferredBy)

* Log Event - tables: Interaction > PersonProjectStatus
* Log Interaction - tables: Interaction > PersonProjectStatus
* Log UseCase - tables: UseCase > PersonProjectStatus

* ???


## Query

* 


## notes
* Create Event table (from Interaction)
  - Type [Task, Interaction] ...later, include Deadline, Gateway, etc.
  - Task is an Event with additional fields: code commit ???
  - meeting being an Interation Type of Event with multiple participants

*/

// Lifecycle
function save_lifecycle(){
  for(let step of defaultSteps){
    defaultLifecycle.LifecycleStep.push(step)
  }
  const testLifecycle = [defaultLifecycle]
  for(const plan of testLifecycle){
      useLifecycle.save({
            Name: plan.Name,
            LifecycleStep: plan.LifecycleStep
          });
    }
}
function get_lifecycles(){
  //Get Lifecycles with associated Step names
  const plans = useLifecycle.with('LifecycleStep').get()
  plans.map(item => {
    item.LifecycleStep = item.LifecycleStep.map(step => { return step.Name })
  }) 
  return plans
}
function get_lifecycles_with_projects(){
  //Get Lifecycles with associated Projects
  const plans = useLifecycle.all()
  const projects = useProject.with('Lifecycle').get()
  for(const plan of plans){
    const selected_projects = projects.filter(item => item.LifecycleId == plan.id)
    plan.Projects = selected_projects.length
    delete plan.LifecycleStep
  }
  return plans
}

// Projects
function save_project(){
  const plans = get_lifecycles()
  populateProjectTestData(useProject, plans[0].id)
}
function get_projects(){
  const projects = useProject.with('Lifecycle').get()
  projects.map(item => {
    item.Lifecycle = item.Lifecycle.Name 
  }) 
  return projects
}

// Contacts
function save_persons(){
  const ProjectName = useProject.all()[0].Name
  const selectedProject = useProject.all().filter(item => item.Name == ProjectName)[0]
  const referredByName = ''
  const referredBy = usePerson.all().filter(item => item.Fullname == referredByName)[0]
  populateContactTestData(usePerson, selectedProject, referredBy)
}
function get_persons_with_nested_status(){
  const persons = usePerson.with('PersonProjectStatus', (query)=>{query.with('StepStatus')}).get()
  return persons
}

// Events
function save_event(){
  const ProjectName = useProject.all()[0].Name
  const selectedProject = useProject.all().filter(item => item.Name == ProjectName)[0]
  const participants = usePerson.all().slice(0,2)
  populateEventTestData(useEvent, usePersonProjectStatus, selectedProject, participants)
}
function get_events(){
  const result = useEvent.all()
  return result
}

// Feedback
function save_feedbacks(){
  populateFeedbackTestData(useFeedback, usePersonProjectStatus, usePerson)
}
function get_feedbacks(){
  const feedbacks = useFeedback.all()
  return feedbacks
}






</script>