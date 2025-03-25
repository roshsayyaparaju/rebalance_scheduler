// frontend/src/components/TaskDashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Row, Col, Nav, Button, Spinner, Badge, Alert } from 'react-bootstrap';
import SignOffModal from './SignOffModal';

const TaskDashboard = () => {
    // State variables
    const [companies, setCompanies] = useState([]);
    const [timeSlots, setTimeSlots] = useState([]);
    const [teamMembers, setTeamMembers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeTimeSlotId, setActiveTimeSlotId] = useState(null);
    const [showSignOffModal, setShowSignOffModal] = useState(false);
    const [selectedTaskGroup, setSelectedTaskGroup] = useState(null);
    const [currentDate, setCurrentDate] = useState(new Date().toISOString().split('T')[0]);
    const [taskHistory, setTaskHistory] = useState([]);
    const [isToday, setIsToday] = useState(true);

    // Check if a date is today
    const checkIfToday = (dateString) => {
        const date = new Date(dateString);
        date.setHours(0, 0, 0, 0);
        
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        return date.getTime() === today.getTime();
    };

    // Format date for display
    const formatDisplayDate = (dateString) => {
        const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    // Load initial data on component mount
    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                setLoading(true);
                
                // Fetch time slots and team members
                const [timeSlotsRes, teamMembersRes, historyRes] = await Promise.all([
                    axios.get('http://localhost:8000/api/time-slots/'),
                    axios.get('http://localhost:8000/api/team-members/'),
                    axios.get('http://localhost:8000/api/task-history/')
                ]);
                
                // Sort time slots by order
                const sortedTimeSlots = timeSlotsRes.data.sort((a, b) => a.order - b.order);
                setTimeSlots(sortedTimeSlots);
                
                // Set the first time slot as active
                if (sortedTimeSlots.length > 0 && !activeTimeSlotId) {
                    setActiveTimeSlotId(sortedTimeSlots[0].id);
                }
                
                setTeamMembers(teamMembersRes.data);
                setTaskHistory(historyRes.data);
                
                // Check if current date is today
                setIsToday(checkIfToday(currentDate));
                
                setLoading(false);
            } catch (err) {
                setError("Failed to load initial data. Please refresh the page.");
                setLoading(false);
                console.error('Error loading initial data:', err);
            }
        };
        
        fetchInitialData();
    }, []);

    // Fetch tasks whenever time slot or date changes
    useEffect(() => {
        const fetchTasks = async () => {
            if (!activeTimeSlotId) return;
            
            try {
                setLoading(true);
                
                // Fetch companies with tasks for the selected time slot and date
                const response = await axios.get(
                    `http://localhost:8000/api/companies/with_tasks/?time_slot=${activeTimeSlotId}&date=${currentDate}`
                );
                
                // Only include companies with tasks for this time slot
                const companiesWithTasks = response.data.filter(
                    company => company.task_groups && company.task_groups.length > 0
                );
                
                setCompanies(companiesWithTasks);
                setLoading(false);
            } catch (err) {
                setError("Failed to load tasks. Please try again.");
                setLoading(false);
                console.error('Error loading tasks:', err);
            }
        };
        
        fetchTasks();
    }, [activeTimeSlotId, currentDate]);

    // Handle time slot tab click
    const handleTimeSlotClick = (timeSlotId) => {
        setActiveTimeSlotId(timeSlotId);
    };

    // Handle sign off button click
    const handleSignOffClick = (taskGroup) => {
        setSelectedTaskGroup(taskGroup);
        setShowSignOffModal(true);
    };

    // Handle sign off completion
    const handleSignOffComplete = async (taskGroupId, teamMemberId, notes) => {
        try {
            await axios.post('http://localhost:8000/api/task-signoffs/sign_off/', {
                task_group_id: taskGroupId,
                team_member_id: teamMemberId,
                notes: notes,
                completed_date: currentDate
            });

            // Refresh task data
            const response = await axios.get(
                `http://localhost:8000/api/companies/with_tasks/?time_slot=${activeTimeSlotId}&date=${currentDate}`
            );
            
            const companiesWithTasks = response.data.filter(
                company => company.task_groups && company.task_groups.length > 0
            );
            
            setCompanies(companiesWithTasks);
            
            // Refresh history
            const historyRes = await axios.get('http://localhost:8000/api/task-history/');
            setTaskHistory(historyRes.data);
            
            // Close modal
            setShowSignOffModal(false);
        } catch (err) {
            console.error('Error signing off task:', err);
            alert('Failed to sign off task. Please try again.');
        }
    };

    // Navigation to previous day
    const goToPreviousDay = () => {
        const date = new Date(currentDate);
        date.setDate(date.getDate() - 1);
        setCurrentDate(date.toISOString().split('T')[0]);
        setIsToday(checkIfToday(date.toISOString().split('T')[0]));
    };

    // Navigation to today
    const goToToday = () => {
        const today = new Date();
        setCurrentDate(today.toISOString().split('T')[0]);
        setIsToday(true);
    };

    // Render loading spinner
    if (loading) {
        return (
            <div className="d-flex justify-content-center my-5">
                <Spinner animation="border" variant="primary" />
            </div>
        );
    }

    // Render error message
    if (error) {
        return (
            <Alert variant="danger" className="my-3">
                {error}
            </Alert>
        );
    }

    return (
        <div>
            {/* Dashboard header with date navigation */}
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h2>Task Dashboard</h2>
                <div className="d-flex align-items-center">
                    <Button 
                        variant="outline-secondary" 
                        size="sm" 
                        onClick={goToPreviousDay}
                    >
                        Previous Day
                    </Button>
                    <h4 className="mx-3 mb-0">{formatDisplayDate(currentDate)}</h4>
                    {!isToday && (
                        <Button 
                            variant="outline-primary" 
                            size="sm" 
                            onClick={goToToday}
                        >
                            Today
                        </Button>
                    )}
                </div>
            </div>

            {/* Time slot tabs */}
            <Nav variant="tabs" className="mb-4">
                {timeSlots.map(timeSlot => (
                    <Nav.Item key={timeSlot.id}>
                        <Nav.Link 
                            active={activeTimeSlotId === timeSlot.id}
                            onClick={() => handleTimeSlotClick(timeSlot.id)}
                        >
                            {timeSlot.name}
                        </Nav.Link>
                    </Nav.Item>
                ))}
            </Nav>

            <Row>
                {/* Main content area */}
                <Col md={8}>
                    {companies.length > 0 ? (
                        companies.map(company => (
                            <Card key={company.id} className="mb-4">
                                <Card.Header className="bg-primary text-white">
                                    <h5 className="mb-0">{company.name}</h5>
                                </Card.Header>
                                <Card.Body>
                                    {company.task_groups.map(taskGroup => (
                                        <Card key={taskGroup.id} className="mb-3">
                                            <Card.Header className="d-flex justify-content-between align-items-center">
                                                <div>
                                                    <h6 className="mb-0">{taskGroup.name}</h6>
                                                    {taskGroup.dallas_time && (
                                                        <small className="text-muted">
                                                            Dallas Time: {taskGroup.dallas_time}
                                                        </small>
                                                    )}
                                                </div>
                                                <div>
                                                    {taskGroup.latest_signoff ? (
                                                        <Badge bg="success" className="me-2">
                                                            Signed off by {taskGroup.latest_signoff.team_member_name}
                                                        </Badge>
                                                    ) : (
                                                        <Button 
                                                            variant="primary" 
                                                            size="sm"
                                                            onClick={() => handleSignOffClick(taskGroup)}
                                                            disabled={!isToday}
                                                        >
                                                            Sign Off
                                                        </Button>
                                                    )}
                                                </div>
                                            </Card.Header>
                                            {taskGroup.tasks && taskGroup.tasks.length > 0 && (
                                                <Card.Body>
                                                    <ul className="list-group task-list">
                                                        {taskGroup.tasks.map(task => (
                                                            <li key={task.id} className="list-group-item border-0 px-0 py-1">
                                                                {task.description}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </Card.Body>
                                            )}
                                        </Card>
                                    ))}
                                </Card.Body>
                            </Card>
                        ))
                    ) : (
                        <Alert variant="info">
                            No tasks found for the selected time slot.
                        </Alert>
                    )}
                </Col>

                {/* Sidebar with sign-off history */}
                <Col md={4}>
                    <Card>
                        <Card.Header className="bg-secondary text-white">
                            <h5 className="mb-0">Recent Sign-Offs</h5>
                        </Card.Header>
                        <Card.Body>
                            {taskHistory.length > 0 ? (
                                <div className="history-list">
                                    {taskHistory.slice(0, 10).map(signoff => (
                                        <div key={signoff.id} className="history-item border-bottom py-2">
                                            <div className="d-flex justify-content-between">
                                                <strong>{signoff.task_group_name}</strong>
                                                <small className="text-muted">
                                                    {new Date(signoff.sign_off_date).toLocaleDateString()}
                                                </small>
                                            </div>
                                            <div>
                                                <Badge bg="info">{signoff.company_name}</Badge>
                                                <span className="ms-2">Signed by: {signoff.team_member_name}</span>
                                            </div>
                                            {signoff.notes && (
                                                <div className="mt-1">
                                                    <small>{signoff.notes}</small>
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-center text-muted">No recent sign-offs found.</p>
                            )}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            {/* Sign off modal */}
            {showSignOffModal && (
                <SignOffModal
                    show={showSignOffModal}
                    onHide={() => setShowSignOffModal(false)}
                    taskGroup={selectedTaskGroup}
                    teamMembers={teamMembers}
                    onComplete={handleSignOffComplete}
                />
            )}
        </div>
    );
};

export default TaskDashboard;