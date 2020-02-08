import React, { useState, useEffect } from 'react';
import {createProject, deleteProject} from "../../api/project"

const ProjectCreate  = (props)  => {

    const [classes, setCLasses] = useState([]);
    const [name, setName] = useState("");
    const [description, setDescription] = useState("")
    const classInputValue = React.createRef();


    const handleChange = (e) => {
        if (e.target.name === "name") {
            setName(e.target.value)
        } else if(e.target.name === "description") {
            setDescription(e.target.value)
        }
    }
    const addClass = (e) => {
        e.preventDefault();
        const newClassName = classInputValue.current.value;
        try {
              if (newClassName === "") {
                throw new Error("Please add a name")
            }
                if (classes.filter(class_ => class_.label === newClassName).length) {
                   throw new Error('Class already in included')
                }
             const searchTerm = prompt("enter search term");
             const class_ = {
                 label: newClassName,
                 search_term: searchTerm,
                 max_images: 1000
             }
            setCLasses([...classes, class_]);
            classInputValue.current.value = ""
        } catch (e) {
            console.log(e.message)
            alert(e.message)
        }
    }

    const renderClasses = () => {
        return (
            classes.map((item) => {
                return <li className="tag">{item.label}</li>
            })
        )
    }

    const createProjectCall = async (e) => {
        e.preventDefault();
         try {
             const data = {
                 name,
                 description,
                 classes
             }

            const res = await createProject(data);
             props.fetchAllProjects();
             props.toggleProjectCreate();


         } catch (e) {
             console.log(e)
             alert("error creating project")
         }
    }
        return (
            <form className="project-create">
                <div>
                    <label>Project Name</label> <br/>
                     <input onChange={handleChange} type="text" name="name"/>
                </div>
                <div>
                    <label>Project Description</label> <br/>
                    <input onChange={handleChange} type="text" name="description"/>
                </div>
                <div style={{textAlign: 'center'}}>
                    <label>Project Classes</label> <br/>
                    <ul style={{display: 'flex', flexDirection: 'row'}}>
                        {renderClasses()}
                    </ul>
                    <div>
                        <input style={{width: '50%'}} ref={classInputValue} type="text" placeholder="class name"/>
                        <button onClick={addClass} style={{marginLeft: "5px"}} className="button">Add Class</button>
                    </div>
                </div>
                <button style={{marginTop: '5rem', width: "100%", backgroundColor: "green"}}  onClick={createProjectCall} className="button">Create Project</button>
            </form>
        )
}

export default ProjectCreate;