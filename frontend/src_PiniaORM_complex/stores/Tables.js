import { Model } from 'pinia-orm'
import { ArrayCast, StringCast, DateCast } from 'pinia-orm/casts';
import { useDisplayStore } from '@/main';


// Person, Project, PersonProjectStatus

export class Person extends Model {
  static entity = 'Person'
  static fields () {
    return {
      id: this.uid(),
      Fullname: this.string(""),
      Title: this.string(""),
      Email: this.string(""),
      Number: this.string(""),
      Office: this.string(""),
      Firm: this.string(""),
      //Projects: this.attr([""]),
      Statuses: this.hasMany(PersonProjectStatus, 'StatusId'),   //insert with ReferredBy for selected Project
      // collect with repos
      //ReferencesGiven: this.hasMany(PersonProjectStatus , 'RefId'),
      //Interactions: this.hasMany(Interaction, 'ParticipantsId'),    
      //UseCases: this.hasMany(Interaction, 'ParticipantsId'),        
    }
  }
}

//import { Interaction } from '@/stores/Interaction';
//import { UseCase } from '@/stores/UseCase.js';

export class PersonProjectStatus extends Model {
    static entity = 'PersonProjectStatus'
    //static primaryKey = ['StatusId', 'Person', 'Project']
    static fields(){
        return{
            id: this.uid(),
            StatusId: this.attr(null),
            //PersonId: this.attr(null),
            //Person: this.belongsTo(Person, 'PersonId'),
            ProjectId: this.attr(null),
            Project: this.belongsTo(Project, 'ProjectId'),
            RefId: this.attr(null),
            ReferredBy: this.belongsTo(Person, 'RefId'),
            CurrentLifecycleStep: this.string(""),
            //LifecycleStepIds: this.attr([]),
            LifecycleSteps: this.hasMany(StepStatus, 'StepId'),
            // collections
            //Interactions: this.hasMany(Interaction, 'InteractionId'),
            //UseCases: this.hasMany(UseCase, 'UseCaseId'),
        }
    }
    static mutators(){
      return {
        Step:{
          get: () => {
            //get the most-recent of LifecycleSteps: TODO: how ???
            //if(useDisplayStore.project.availableStatus.includes(value)){
              return value
        }
      }
    }
  }
}

export class StepStatus extends Model {
  static entity = 'stepStatus'
  static fields () {
    return {
      id: this.uid(),
      StepId: this.attr(null),
      LifecycleStepId: this.attr(),
      LifecycleStep: this.belongsTo(LifecycleStep, 'LifecycleStepId'),
      StatusDate: this.attr()
    }
  }
  static casts(){
    return {
      StatusDate: DateCast,
    }
  }
}


/*
class StepStatus extends Model {
  static entity = 'stepStatus'

  static primaryKey = ['StepId', 'LifecycleStepIds']

  static fields () {
    return {
      StepId: this.attr(null),
      LifecycleStepIds: this.attr(null)
    }
  }
}*/










export class Project extends Model {
  static entity = 'Project'
  //static primaryKey = ['id', 'Name']
  static fields(){
    return {
      id: this.uid(),
      Name: this.string(''),
      Status: this.string(useDisplayStore.project.availableStatus[0]),    //different from PersonProjectStatus
      Category: this.string(""),
      StartDate: this.attr(),
      EndDate: this.attr(),
      LifecycleId: this.attr(null),
      Lifecycle: this.belongsTo(Lifecycle, 'LifecycleId'),
      Repos: this.string("")
    }
  }
  static casts(){
    return {
      Status: StringCast,
      Category: StringCast,
      StartDate: DateCast,
      EndDate: DateCast
    }
  }
  static mutators(){
    return {
      Status:{
        set: (value) => {
          if(useDisplayStore.project.availableStatus.includes(value)){
            return value
          }
        }
      }
    }
  }
}





// Interaction, UseCase, Lifecycle

export class Interaction extends Model {
    static entity = 'Interaction'
    static fields(){
        return{
            id: this.uid(),
            InteractionId: this.attr(),
            //PersonProject: this.belongsTo(PersonProjectStatus, 'InteractionId'),
            //LifecycleStep: this.string(""),
            Participants: this.hasMany(Person, 'id'),    //no corresponding Person belongsTo()
            Datetime: this.attr(),
            Comments: this.string(""),
        }
    }
    static casts(){
        return {
          Participants: ArrayCast,
          Datetime: DateCast,
          Comments: StringCast
        }
    }
    static mutators(){
        return {
          Status:{
            set: (value) => {
              if(useDisplayStore.project.availableStatus.includes(value)){
                return value
              }
            }
          }
        }
      }
}


export class UseCase extends Model {
    static entity = 'UseCase'
    static fields(){
        return{
            id: this.uid(),
            UseCaseId: this.uid(),
            PersonProject: this.belongsTo(PersonProjectStatus, 'UseCaseId'),
            Role: this.string(""),
            Use: this.string(""),
            PainPoint: this.string("")
        }
    }
    static casts(){
        return {
          Role: StringCast,
          Use: StringCast,
          PainPoint: StringCast
        }
    }
}



//import { defaultSteps, defaultLifecycle } from '../assets/defaults.js'

export class Lifecycle extends Model {
  static entity = 'Lifecycle'
  static fields () {
    return {
      id: this.uid(),
      Name: this.string('').notNullable(),
      Projects: this.hasMany(Project, 'id'),
      LifecycleStep: this.hasMany(LifecycleStep, 'StepId')
    }
  }
}

export class LifecycleStep extends Model {
  static entity = 'LifecycleStep'
  static fields () {
    return {
      id: this.uid(),
      StepId: this.attr(null),
      Name: this.string('').notNullable(),
      DurationBizDays: this.number(),
      Order: this.number(),
      Placeholder: this.attr([]),
      EmailForm: this.string('')
    }
  }
  static casts () {
    return {
        Placeholder: ArrayCast
    }
  }
  get parsePlaceholder(){
    const ph = JSON.parse(this.Placeholder)
    return {
      id: this.id, 
      Name: this.Name,
      DurationBizDays: this.DurationBizDays,
      Order: this.Order, 
      Placeholder: ph, 
      EmailForm: this.EmailForm
    }
  }
}







// Account

export class Account extends Model {
  static entity = 'Account'
  static fields () {
    return {
      id: this.uid(),
      Fullname: this.string("")
    }
  }
}