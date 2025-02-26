// frontend/src/components/JobModal.js
import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const JobModal = ({ job, teamMembers, onAssign, onClose }) => {
    const [selectedMemberId, setSelectedMemberId] = useState(job.assigned_to || '');

    const handleSubmit = (e) => {
        e.preventDefault();
        onAssign(job.id, selectedMemberId || null);
    };

    return (
        <Modal show={true} onHide={onClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>{job.title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div className="mb-3">
                    <p><strong>Index:</strong> {job.index_name}</p>
                    <p>
                        <strong>Time:</strong> {job.start.toLocaleString()} - {job.end.toLocaleString()}
                    </p>
                    {job.notes && (
                        <p><strong>Notes:</strong> {job.notes}</p>
                    )}
                    <p>
                        <strong>Currently Assigned To:</strong>{' '}
                        {job.assigned_to_name || 'Unassigned'}
                    </p>
                </div>

                <Form onSubmit={handleSubmit}>
                    <Form.Group className="mb-3">
                        <Form.Label>Assign To</Form.Label>
                        <Form.Select
                            value={selectedMemberId}
                            onChange={(e) => setSelectedMemberId(e.target.value)}
                        >
                            <option value="">-- Unassigned --</option>
                            {teamMembers.map(member => (
                                <option key={member.id} value={member.id}>
                                    {member.name}
                                </option>
                            ))}
                        </Form.Select>
                    </Form.Group>

                    <div className="d-flex justify-content-end gap-2">
                        <Button variant="secondary" onClick={onClose}>
                            Cancel
                        </Button>
                        <Button variant="primary" type="submit">
                            Save Assignment
                        </Button>
                    </div>
                </Form>
            </Modal.Body>
        </Modal>
    );
};

export default JobModal;