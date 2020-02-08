import axios from "axios";


const getAllProjects = () => {
   return axios.get('/api/projects/classification_project/all');
}

const deleteProject = (id) => {
   return axios.delete(`/api/projects/classification_project?_id=${id}`);
}

const createProject = (data) => {
   return axios.post("/api/projects/classification_project", data)
}

const collectData = (id) => {
   return axios.post(`/api/projects/classification_project/collect_google_images?_id=${id}`)
}

const trainProject = (id) => {
   return axios.post(`/api/train?_id=${id}`)
}



export {getAllProjects, deleteProject, createProject, collectData, trainProject}