// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract ProjectStatus is Ownable, Pausable, ReentrancyGuard {
    struct Status {
        string status;
        uint256 progress;
        string metrics;
        uint256 timestamp;
    }
    
    struct Milestone {
        string name;
        string description;
        uint256 targetDate;
        uint256 completionDate;
        string status;
        bool exists;
    }
    
    struct Alert {
        string alertType;
        string message;
        string severity;
        uint256 timestamp;
        bool resolved;
    }
    
    mapping(string => Status[]) public projectStatusHistory;
    mapping(string => mapping(string => Milestone)) public projectMilestones;
    mapping(string => Alert[]) public projectAlerts;
    mapping(string => bool) public projectExists;
    
    event ProjectStatusUpdated(string projectId, string status, uint256 progress);
    event MilestoneAdded(string projectId, string milestoneName);
    event MilestoneStatusUpdated(string projectId, string milestoneName, string status);
    event AlertAdded(string projectId, string alertType, string severity);
    
    constructor() {
        // Initialize contract
    }
    
    function createProjectStatus(
        string memory _projectId,
        string memory _status,
        uint256 _progress,
        string memory _metrics
    ) external whenNotPaused nonReentrant {
        require(bytes(_projectId).length > 0, "Project ID cannot be empty");
        require(bytes(_status).length > 0, "Status cannot be empty");
        require(_progress <= 100, "Progress cannot exceed 100");
        
        projectExists[_projectId] = true;
        
        projectStatusHistory[_projectId].push(Status({
            status: _status,
            progress: _progress,
            metrics: _metrics,
            timestamp: block.timestamp
        }));
        
        emit ProjectStatusUpdated(_projectId, _status, _progress);
    }
    
    function updateProjectProgress(
        string memory _projectId,
        uint256 _progress,
        string memory _metrics
    ) external whenNotPaused nonReentrant {
        require(projectExists[_projectId], "Project does not exist");
        require(_progress <= 100, "Progress cannot exceed 100");
        
        Status[] storage history = projectStatusHistory[_projectId];
        require(history.length > 0, "No status history found");
        
        Status memory lastStatus = history[history.length - 1];
        
        projectStatusHistory[_projectId].push(Status({
            status: lastStatus.status,
            progress: _progress,
            metrics: _metrics,
            timestamp: block.timestamp
        }));
        
        emit ProjectStatusUpdated(_projectId, lastStatus.status, _progress);
    }
    
    function getProjectStatus(string memory _projectId) external view returns (Status memory) {
        require(projectExists[_projectId], "Project does not exist");
        Status[] storage history = projectStatusHistory[_projectId];
        require(history.length > 0, "No status history found");
        return history[history.length - 1];
    }
    
    function getProjectHistory(string memory _projectId) external view returns (Status[] memory) {
        require(projectExists[_projectId], "Project does not exist");
        return projectStatusHistory[_projectId];
    }
    
    function addProjectMilestone(
        string memory _projectId,
        string memory _milestoneName,
        string memory _description,
        uint256 _targetDate
    ) external whenNotPaused nonReentrant {
        require(projectExists[_projectId], "Project does not exist");
        require(bytes(_milestoneName).length > 0, "Milestone name cannot be empty");
        require(!projectMilestones[_projectId][_milestoneName].exists, "Milestone already exists");
        require(_targetDate > block.timestamp, "Target date must be in the future");
        
        projectMilestones[_projectId][_milestoneName] = Milestone({
            name: _milestoneName,
            description: _description,
            targetDate: _targetDate,
            completionDate: 0,
            status: "pending",
            exists: true
        });
        
        emit MilestoneAdded(_projectId, _milestoneName);
    }
    
    function updateMilestoneStatus(
        string memory _projectId,
        string memory _milestoneName,
        string memory _status,
        uint256 _completionDate
    ) external whenNotPaused nonReentrant {
        require(projectExists[_projectId], "Project does not exist");
        require(projectMilestones[_projectId][_milestoneName].exists, "Milestone does not exist");
        
        Milestone storage milestone = projectMilestones[_projectId][_milestoneName];
        milestone.status = _status;
        if (_completionDate > 0) {
            milestone.completionDate = _completionDate;
        }
        
        emit MilestoneStatusUpdated(_projectId, _milestoneName, _status);
    }
    
    function getProjectMilestones(string memory _projectId) external view returns (Milestone[] memory) {
        require(projectExists[_projectId], "Project does not exist");
        
        // Count existing milestones
        uint256 count = 0;
        for (uint256 i = 0; i < 100; i++) { // Assuming max 100 milestones per project
            string memory milestoneName = string(abi.encodePacked("milestone_", i));
            if (projectMilestones[_projectId][milestoneName].exists) {
                count++;
            }
        }
        
        // Create array of milestones
        Milestone[] memory milestones = new Milestone[](count);
        uint256 index = 0;
        
        for (uint256 i = 0; i < 100; i++) {
            string memory milestoneName = string(abi.encodePacked("milestone_", i));
            if (projectMilestones[_projectId][milestoneName].exists) {
                milestones[index] = projectMilestones[_projectId][milestoneName];
                index++;
            }
        }
        
        return milestones;
    }
    
    function addProjectAlert(
        string memory _projectId,
        string memory _alertType,
        string memory _message,
        string memory _severity
    ) external whenNotPaused nonReentrant {
        require(projectExists[_projectId], "Project does not exist");
        require(bytes(_alertType).length > 0, "Alert type cannot be empty");
        require(bytes(_message).length > 0, "Message cannot be empty");
        require(bytes(_severity).length > 0, "Severity cannot be empty");
        
        projectAlerts[_projectId].push(Alert({
            alertType: _alertType,
            message: _message,
            severity: _severity,
            timestamp: block.timestamp,
            resolved: false
        }));
        
        emit AlertAdded(_projectId, _alertType, _severity);
    }
    
    function getProjectAlerts(string memory _projectId) external view returns (Alert[] memory) {
        require(projectExists[_projectId], "Project does not exist");
        return projectAlerts[_projectId];
    }
    
    function pause() external onlyOwner {
        _pause();
    }
    
    function unpause() external onlyOwner {
        _unpause();
    }
} 