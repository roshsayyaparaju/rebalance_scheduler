// frontend/src/components/Indexes.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Table, Button, Form, Modal } from 'react-bootstrap';

const Indexes = () => {
    const [indexes, setIndexes] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        description: ''
    });
    const [editMode, setEditMode] = useState(false);
    const [currentId, setCurrentId] = useState(null);

    // Fetch indexes on component mount
    useEffect(() => {
        fetchIndexes();
    }, []);

    const fetchIndexes = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/indexes/');
            setIndexes(response.data);
        } catch (error) {
            console.error('Error fetching indexes:', error);
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
                await axios.put(`http://localhost:8000/api/indexes/${currentId}/`, formData);
            } else {
                await axios.post('http://localhost:8000/api/indexes/', formData);
            }
            fetchIndexes();
            handleCloseModal();
        } catch (error) {
            console.error('Error saving index:', error);
        }
    };

    const handleEdit = (index) => {
        setFormData({
            name: index.name,
            description: index.description
        });
        setCurrentId(index.id);
        setEditMode(true);
        setShowModal(true);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this index? This will also delete all associated jobs.')) {
            try {
                await axios.delete(`http://localhost:8000/api/indexes/${id}/`);
                fetchIndexes();
            } catch (error) {
                console.error('Error deleting index:', error);
            }
        }
    };

    const handleCloseModal = () => {
        setShowModal(false);
        setFormData({ name: '', description: '' });
        setEditMode(false);
        setCurrentId(null);
    };

    return (
        <div>
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Indexes</h2>
                <Button variant="primary" onClick={() => setShowModal(true)}>
                    Add Index
                </Button>
            </div>

            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {indexes.map(index => (
                        <tr key={index.id}>
                            <td>{index.name}</td>
                            <td>{index.description}</td>
                            <td>
                                <Button variant="outline-primary" size="sm" className="me-2" onClick={() => handleEdit(index)}>
                                    Edit
                                </Button>
                                <Button variant="outline-danger" size="sm" onClick={() => handleDelete(index.id)}>
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
                    <Modal.Title>{editMode ? 'Edit' : 'Add'} Index</Modal.Title>
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
                            <Form.Label>Description</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                name="description"
                                value={formData.description}
                                onChange={handleInputChange}
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

export default Indexes;