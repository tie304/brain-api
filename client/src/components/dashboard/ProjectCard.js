import React, { Component } from 'react';



const ProjectCard = (props) => {

        const deleteProject = () => {
            if (window.confirm("are you sure? All data will be deleted.")) {
                props.delete(props.project.id)
            }
        }

        const collectData = () => {
            props.collect(props.project.id)
        }

        const trainData = () => {
            props.train(props.project.id)
        }

        return (
            <li className="project-card">
                <h1 className="project-card__title"> {props.project.name}</h1>
                <p className="project-card__description">{props.project.description}</p>
                <ul className="project-card__tags">
                    {props.project.classes.map((class_, idx) => {
                        return <li key={idx}>{class_.label}</li>
                    })}
                </ul>
                <br/>
                <div className="project-card__actions">
                    <button onClick={deleteProject} className="button button--danger">Delete</button>
                    <button onClick={collectData} className="button button--blue">Collect</button>
                    <button onClick={trainData} className="button button--blue">Train</button>
                </div>
            </li>
        )
}

export default ProjectCard;