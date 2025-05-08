// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ContributionCalculator {
    struct ContributionMetrics {
        uint256 baseAmount;
        uint256 multiplier;
        uint256 bonus;
    }
    
    mapping(string => ContributionMetrics) public contributionTypes;
    
    constructor() {
        // Initialize contribution types with base amounts and multipliers
        contributionTypes["planting"] = ContributionMetrics({
            baseAmount: 100 * 10**18,  // 100 tokens
            multiplier: 1,
            bonus: 0
        });
        
        contributionTypes["maintenance"] = ContributionMetrics({
            baseAmount: 50 * 10**18,   // 50 tokens
            multiplier: 1,
            bonus: 0
        });
        
        contributionTypes["monitoring"] = ContributionMetrics({
            baseAmount: 30 * 10**18,   // 30 tokens
            multiplier: 1,
            bonus: 0
        });
        
        contributionTypes["research"] = ContributionMetrics({
            baseAmount: 200 * 10**18,  // 200 tokens
            multiplier: 1,
            bonus: 0
        });
    }
    
    function calculateContributionAmount(
        string memory _contributionType,
        string memory _data
    ) public view returns (uint256) {
        require(contributionTypes[_contributionType].baseAmount > 0, "Invalid contribution type");
        
        ContributionMetrics memory metrics = contributionTypes[_contributionType];
        uint256 amount = metrics.baseAmount;
        
        // Apply multiplier based on contribution data
        if (keccak256(bytes(_contributionType)) == keccak256(bytes("planting"))) {
            amount = calculatePlantingAmount(_data, amount);
        } else if (keccak256(bytes(_contributionType)) == keccak256(bytes("maintenance"))) {
            amount = calculateMaintenanceAmount(_data, amount);
        } else if (keccak256(bytes(_contributionType)) == keccak256(bytes("monitoring"))) {
            amount = calculateMonitoringAmount(_data, amount);
        } else if (keccak256(bytes(_contributionType)) == keccak256(bytes("research"))) {
            amount = calculateResearchAmount(_data, amount);
        }
        
        return amount;
    }
    
    function calculatePlantingAmount(string memory _data, uint256 _baseAmount) internal pure returns (uint256) {
        // Parse data to get number of plants and species
        // Example data format: "{"plants": 10, "species": "drought_resistant"}"
        bytes memory data = bytes(_data);
        uint256 plants = 0;
        string memory species = "";
        
        // Simple parsing (in production, use proper JSON parsing)
        for (uint i = 0; i < data.length; i++) {
            if (data[i] == bytes1('"')) {
                // Extract number of plants
                uint256 start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                string memory plantsStr = substring(_data, start, i);
                plants = stringToUint(plantsStr);
                
                // Extract species
                while (i < data.length && data[i] != bytes1('"')) i++;
                start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                species = substring(_data, start, i);
            }
        }
        
        // Calculate amount based on number of plants and species
        uint256 multiplier = 1;
        if (keccak256(bytes(species)) == keccak256(bytes("drought_resistant"))) {
            multiplier = 2;
        }
        
        return _baseAmount * plants * multiplier;
    }
    
    function calculateMaintenanceAmount(string memory _data, uint256 _baseAmount) internal pure returns (uint256) {
        // Parse data to get maintenance type and duration
        // Example data format: "{"type": "watering", "duration": 3600}"
        bytes memory data = bytes(_data);
        string memory maintenanceType = "";
        uint256 duration = 0;
        
        // Simple parsing (in production, use proper JSON parsing)
        for (uint i = 0; i < data.length; i++) {
            if (data[i] == bytes1('"')) {
                // Extract maintenance type
                uint256 start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                maintenanceType = substring(_data, start, i);
                
                // Extract duration
                while (i < data.length && data[i] != bytes1('"')) i++;
                start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                string memory durationStr = substring(_data, start, i);
                duration = stringToUint(durationStr);
            }
        }
        
        // Calculate amount based on maintenance type and duration
        uint256 multiplier = 1;
        if (keccak256(bytes(maintenanceType)) == keccak256(bytes("watering"))) {
            multiplier = 2;
        }
        
        return _baseAmount * (duration / 3600) * multiplier;
    }
    
    function calculateMonitoringAmount(string memory _data, uint256 _baseAmount) internal pure returns (uint256) {
        // Parse data to get monitoring type and area
        // Example data format: "{"type": "soil_analysis", "area": 1000}"
        bytes memory data = bytes(_data);
        string memory monitoringType = "";
        uint256 area = 0;
        
        // Simple parsing (in production, use proper JSON parsing)
        for (uint i = 0; i < data.length; i++) {
            if (data[i] == bytes1('"')) {
                // Extract monitoring type
                uint256 start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                monitoringType = substring(_data, start, i);
                
                // Extract area
                while (i < data.length && data[i] != bytes1('"')) i++;
                start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                string memory areaStr = substring(_data, start, i);
                area = stringToUint(areaStr);
            }
        }
        
        // Calculate amount based on monitoring type and area
        uint256 multiplier = 1;
        if (keccak256(bytes(monitoringType)) == keccak256(bytes("soil_analysis"))) {
            multiplier = 2;
        }
        
        return _baseAmount * (area / 100) * multiplier;
    }
    
    function calculateResearchAmount(string memory _data, uint256 _baseAmount) internal pure returns (uint256) {
        // Parse data to get research type and complexity
        // Example data format: "{"type": "species_adaptation", "complexity": 3}"
        bytes memory data = bytes(_data);
        string memory researchType = "";
        uint256 complexity = 0;
        
        // Simple parsing (in production, use proper JSON parsing)
        for (uint i = 0; i < data.length; i++) {
            if (data[i] == bytes1('"')) {
                // Extract research type
                uint256 start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                researchType = substring(_data, start, i);
                
                // Extract complexity
                while (i < data.length && data[i] != bytes1('"')) i++;
                start = i + 1;
                while (i < data.length && data[i] != bytes1('"')) i++;
                string memory complexityStr = substring(_data, start, i);
                complexity = stringToUint(complexityStr);
            }
        }
        
        // Calculate amount based on research type and complexity
        uint256 multiplier = 1;
        if (keccak256(bytes(researchType)) == keccak256(bytes("species_adaptation"))) {
            multiplier = 2;
        }
        
        return _baseAmount * complexity * multiplier;
    }
    
    function substring(string memory str, uint startIndex, uint endIndex) internal pure returns (string memory) {
        bytes memory strBytes = bytes(str);
        bytes memory result = new bytes(endIndex - startIndex);
        for(uint i = startIndex; i < endIndex; i++) {
            result[i - startIndex] = strBytes[i];
        }
        return string(result);
    }
    
    function stringToUint(string memory s) internal pure returns (uint256) {
        bytes memory b = bytes(s);
        uint256 result = 0;
        for(uint i = 0; i < b.length; i++) {
            uint8 c = uint8(b[i]);
            if (c >= 48 && c <= 57) {
                result = result * 10 + (c - 48);
            }
        }
        return result;
    }
} 