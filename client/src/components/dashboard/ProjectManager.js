import React, { useState, useEffect } from 'react';
import { getAllProjects, deleteProject, collectData, trainProject } from "../../api/project"
import ProjectCard from "./ProjectCard";
import ProjectCreate from "./ProjectCreate";



const ProjectManager = (props) => {
    const [projects, setProjects] = useState([]);
    const [createProject, setProjectCreate] = useState(false);


    useEffect(() => {
       getAllProjects().then((res) => {
           setProjects(res.data.projects)
       });

    }, []);


 const deleteProjectById = async (id) => {
     try {
         const res = await deleteProject(id);
         const filteredProjects = projects.filter(project => project.id !== id)
         setProjects(filteredProjects)
     } catch (e) {
         console.log(e)
         alert("error deleting project")
     }
    }

    const fetchAllProjects = async () => {
        const res = await getAllProjects();
         setProjects(res.data.projects)
    }
    const toggleProjectCreate = (e) => {
     setProjectCreate(!createProject)
    }

    const collectDataByProjectId = async (id) => {
        const res = await collectData(id);
    }

    const trainProjectById = async (id) => {
     const res = await trainProject(id);
    }

   if (projects.length === 0) {
       return(
           <section className="dashboard">
               {createProject ?  <ProjectCreate fetchAllProjects={fetchAllProjects} toggleProjectCreate={toggleProjectCreate} />: ""}
               <h1 style={{textAlign: 'center', fontSize: '40px'}}>No Projects Added Yet</h1>
               <div onClick={toggleProjectCreate} className="dashboard__create-project">
                    Add
                </div>
           </section>
       )
   } else {
        return (
        <section className="dashboard">
             {createProject ?  <ProjectCreate fetchAllProjects={fetchAllProjects} toggleProjectCreate={toggleProjectCreate} />: ""}
            <ul className="dashboard__projects">
                {projects.map((project, idx) => {
                    return <ProjectCard project={project} key={idx} delete={deleteProjectById} collect={collectDataByProjectId} train={trainProjectById}/>
                })}
            </ul>
             <div onClick={toggleProjectCreate} className="dashboard__create-project">
                    Add
             </div>

        </section>
    )
   }
}


export default ProjectManager;