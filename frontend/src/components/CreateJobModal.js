// frontend/src/components/CreateJobModal.js
import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import axios from 'axios';

const CreateJobModal = ({ indexes, teamMembers, onClose, onJobCreated, selectedDate }) => {
    const [formData, setFormData] = useState({
        title: '',
        index: '',
        startTime: selectedDate ? new Date(selectedDate) : new Date(),
        endTime: selectedDate ? new Date(new Date(selectedDate).setHours(new Date(selectedDate).getHours() + 2)) : new Date(new Date().setHours(new Date().getHours() + 2)),
        assignedTo: '',
        notes: '',
        color: '#3174ad'
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleDateChange = (date, field) => {
        setFormData({
            ...formData,
            [field]: date
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const jobData = {
                title: formData.title,
                index: formData.index,
                start_time: formData.startTime.toISOString(),
                end_time: formData.endTime.toISOString(),
                assigned_to: formData.assignedTo || null,
                notes: formData.notes,
                color: formData.color
            };

            const response = await axios.post('http://localhost:8000/api/jobs/', jobData);
            onJobCreated(response.data);
            onClose();
        } catch (error) {
            console.error('Error creating job:', error);
            alert('Failed to create job. Please try again.');
        }
    };

    return (
        <Modal show={true} onHide={onClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Create New Job</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleInputChange}
                            placeholder="Enter job title"
                            required
                        />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Index</Form.Label>
                        <Form.Select
                            name="index"
                            value={formData.index}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="">Select an index</option>
                            {indexes.map(index => (
                                <option key={index.id} value={index.id}>
                                    {index.name}
                                </option>
                            ))}
                        </Form.Select>
                    </Form.Group>

                    <div className="row mb-3">
                        <div className="col">
                            <Form.Group>
                                <Form.Label>Start Time</Form.Label>
                                <DatePicker
                                    selected={formData.startTime}
                                    onChange={(date) => handleDateChange(date, 'startTime')}
                                    showTimeSelect
                                    timeFormat="HH:mm"
                                    timeIntervals={15}
                                    dateFormat="MMMM d, yyyy h:mm aa"
                                    className="form-control"
                                    required
                                />
                            </Form.Group>
                        </div>
                        <div className="col">
                            <Form.Group>
                                <Form.Label>End Time</Form.Label>
                                <DatePicker
                                    selected={formData.endTime}
                                    onChange={(date) => handleDateChange(date, 'endTime')}
                                    showTimeSelect
                                    timeFormat="HH:mm"
                                    timeIntervals={15}
                                    dateFormat="MMMM d, yyyy h:mm aa"
                                    className="form-control"
                                    required
                                />
                            </Form.Group>
                        </div>
                    </div>

                    <Form.Group className="mb-3">
                        <Form.Label>Assign To</Form.Label>
                        <Form.Select
                            name="assignedTo"
                            value={formData.assignedTo}
                            onChange={handleInputChange}
                        >
                            <option value="">-- Unassigned --</option>
                            {teamMembers.map(member => (
                                <option key={member.id} value={member.id}>
                                    {member.name}
                                </option>
                            ))}
                        </Form.Select>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Notes</Form.Label>
                        <Form.Control
                            as="textarea"
                            name="notes"
                            value={formData.notes}
                            onChange={handleInputChange}
                            rows={3}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Color</Form.Label>
                        <Form.Control
                            type="color"
                            name="color"
                            value={formData.color}
                            onChange={handleInputChange}
                            title="Choose job color"
                        />
                    </Form.Group>

                    <div className="d-flex justify-content-end gap-2">
                        <Button variant="secondary" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button variant="primary" type="submit">
                            Create Job
                        </Button>
                    </div>
                </Form>
            </Modal.Body>
        </Modal>
    );
};

export default CreateJobModal;