// frontend/src/components/TeamMembers.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Form, Modal } from 'react-bootstrap';

const TeamMembers = () => {
    const [teamMembers, setTeamMembers] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        email: ''
    });
    const [editMode, setEditMode] = useState(false);
    const [currentId, setCurrentId] = useState(null);

    // Fetch team members on component mount
    useEffect(() => {
        fetchTeamMembers();
    }, []);

    const fetchTeamMembers = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/team-members/');
            setTeamMembers(response.data);
        } catch (error) {
            console.error('Error fetching team members:', error);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editMode) {
                await axios.put(`http://localhost:8000/api/team-members/${currentId}/`, formData);
            } else {
                await axios.post('http://localhost:8000/api/team-members/', formData);
            }
            fetchTeamMembers();
            handleCloseModal();
        } catch (error) {
            console.error('Error saving team member:', error);
        }
    };

    const handleEdit = (member) => {
        setFormData({
            name: member.name,
            email: member.email
        });
        setCurrentId(member.id);
        setEditMode(true);
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this team member?')) {
            try {
                await axios.delete(`http://localhost:8000/api/team-members/${id}/`);
                fetchTeamMembers();
            } catch (error) {
                console.error('Error deleting team member:', error);
            }
        }
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setFormData({ name: '', email: '' });
        setEditMode(false);
        setCurrentId(null);
    };

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Team Members</h2>
                <Button variant="primary" onClick={() => setShowModal(true)}>
                    Add Team Member
                </Button>
            </div>

            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {teamMembers.map(member => (
                        <tr key={member.id}>
                            <td>{member.name}</td>
                            <td>{member.email}</td>
                            <td>
                                <Button variant="outline-primary" size="sm" className="me-2" onClick={() => handleEdit(member)}>
                                    Edit
                                </Button>
                                <Button variant="outline-danger" size="sm" onClick={() => handleDelete(member.id)}>
                                    Delete
                                </Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>

            {/* Add/Edit Modal */}
            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>{editMode ? 'Edit' : 'Add'} Team Member</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Name</Form.Label>
                            <Form.Control
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleInputChange}
                                required
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                required
                            />
                        </Form.Group>
                        <div className="d-flex justify-content-end gap-2">
                            <Button variant="secondary" onClick={handleCloseModal}>
                                Cancel
                            </Button>
                            <Button variant="primary" type="submit">
                                Save
                            </Button>
                        </div>
                    </Form>
                </Modal.Body>
            </Modal>
        </div>
    );
};

export default TeamMembers;