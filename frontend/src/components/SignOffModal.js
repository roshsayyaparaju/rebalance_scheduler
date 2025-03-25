// frontend/src/components/SignOffModal.js
import React, { useState } from 'react';
import { Modal, Button, Form, Alert } from 'react-bootstrap';

const SignOffModal = ({ show, onHide, taskGroup, teamMembers, onComplete }) => {
    const [teamMemberId, setTeamMemberId] = useState('');
    const [notes, setNotes] = useState('');
    const [confirmStep, setConfirmStep] = useState(false);
    const [formError, setFormError] = useState('');
    
    // Handle form submission for initial step
    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (!teamMemberId) {
            setFormError('Please select a team member.');
            return;
        }
        
        // Proceed to confirmation step
        setConfirmStep(true);
        setFormError('');
    };
    
    // Handle final confirm button click
    const handleConfirm = () => {
        onComplete(taskGroup.id, teamMemberId, notes);
    };
    
    // Reset the form when modal is closed
    const handleClose = () => {
        setTeamMemberId('');
        setNotes('');
        setConfirmStep(false);
        setFormError('');
        onHide();
    };

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>
                    {confirmStep ? 'Confirm Sign-Off' : 'Sign Off Task'}
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {!confirmStep ? (
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Task Group</Form.Label>
                            <Form.Control
                                type="text"
                                value={`${taskGroup.company_name} - ${taskGroup.name}`}
                                disabled
                            />
                        </Form.Group>
                        
                        <Form.Group className="mb-3">
                            <Form.Label>Team Member</Form.Label>
                            <Form.Select
                                value={teamMemberId}
                                onChange={(e) => setTeamMemberId(e.target.value)}
                                required
                            >
                                <option value="">-- Select Team Member --</option>
                                {teamMembers.map(member => (
                                    <option key={member.id} value={member.id}>
                                        {member.name}
                                    </option>
                                ))}
                            </Form.Select>
                        </Form.Group>
                        
                        <Form.Group className="mb-3">
                            <Form.Label>Notes (Optional)</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                placeholder="Add any notes or comments about this task completion"
                            />
                        </Form.Group>
                        
                        {formError && (
                            <Alert variant="danger" className="mt-3">
                                {formError}
                            </Alert>
                        )}
                        
                        <div className="d-flex justify-content-end gap-2 mt-4">
                            <Button variant="secondary" onClick={handleClose}>
                                Cancel
                            </Button>
                            <Button variant="primary" type="submit">
                                Next
                            </Button>
                        </div>
                    </Form>
                ) : (
                    <div>
                        <Alert variant="warning">
                            <strong>Please confirm:</strong> Have you completed all the tasks and 
                            subtasks for this index?
                        </Alert>
                        
                        <div className="task-details my-3">
                            <h6>Tasks:</h6>
                            <ul className="list-group">
                                {taskGroup.tasks.map(task => (
                                    <li key={task.id} className="list-group-item border-0 px-0 py-1">
                                        {task.description}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        
                        <div className="d-flex justify-content-end gap-2 mt-4">
                            <Button variant="secondary" onClick={() => setConfirmStep(false)}>
                                Back
                            </Button>
                            <Button variant="success" onClick={handleConfirm}>
                                Yes, Sign Off
                            </Button>
                        </div>
                    </div>
                )}
            </Modal.Body>
        </Modal>
    );
};

export default SignOffModal;