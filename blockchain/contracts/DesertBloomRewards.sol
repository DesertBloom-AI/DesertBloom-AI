// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./DesertBloomToken.sol";

contract DesertBloomRewards is Ownable, ReentrancyGuard {
    DesertBloomToken public token;
    
    struct Project {
        string name;
        string location;
        uint256 area;
        uint256 targetCarbon;
        bool isActive;
        uint256 totalRewards;
    }
    
    struct Achievement {
        string metric;
        uint256 value;
        uint256 timestamp;
        bool verified;
    }
    
    mapping(uint256 => Project) public projects;
    mapping(uint256 => Achievement[]) public projectAchievements;
    mapping(uint256 => mapping(address => uint256)) public projectContributions;
    
    uint256 public projectCount;
    
    event ProjectCreated(uint256 indexed projectId, string name);
    event AchievementVerified(uint256 indexed projectId, string metric, uint256 value);
    event RewardsDistributed(uint256 indexed projectId, address indexed contributor, uint256 amount);
    
    constructor(address _tokenAddress) {
        token = DesertBloomToken(_tokenAddress);
    }
    
    function createProject(
        string memory _name,
        string memory _location,
        uint256 _area,
        uint256 _targetCarbon
    ) public onlyOwner returns (uint256) {
        uint256 projectId = projectCount++;
        
        projects[projectId] = Project({
            name: _name,
            location: _location,
            area: _area,
            targetCarbon: _targetCarbon,
            isActive: true,
            totalRewards: 0
        });
        
        emit ProjectCreated(projectId, _name);
        return projectId;
    }
    
    function verifyAchievement(
        uint256 _projectId,
        string memory _metric,
        uint256 _value
    ) public onlyOwner {
        require(projects[_projectId].isActive, "Project is not active");
        
        projectAchievements[_projectId].push(Achievement({
            metric: _metric,
            value: _value,
            timestamp: block.timestamp,
            verified: true
        }));
        
        emit AchievementVerified(_projectId, _metric, _value);
    }
    
    function distributeRewards(
        uint256 _projectId,
        address _contributor,
        uint256 _amount
    ) public onlyOwner nonReentrant {
        require(projects[_projectId].isActive, "Project is not active");
        require(token.balanceOf(address(this)) >= _amount, "Insufficient token balance");
        
        token.transfer(_contributor, _amount);
        projectContributions[_projectId][_contributor] += _amount;
        projects[_projectId].totalRewards += _amount;
        
        emit RewardsDistributed(_projectId, _contributor, _amount);
    }
    
    function getProjectAchievements(uint256 _projectId) public view returns (Achievement[] memory) {
        return projectAchievements[_projectId];
    }
    
    function getProjectContributions(uint256 _projectId, address _contributor) public view returns (uint256) {
        return projectContributions[_projectId][_contributor];
    }
} 