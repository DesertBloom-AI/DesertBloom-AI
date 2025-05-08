// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract DesertBloomToken is ERC20, Ownable, Pausable {
    // Token details
    string public constant TOKEN_NAME = "DesertBloom Token";
    string public constant TOKEN_SYMBOL = "DBT";
    uint256 public constant TOTAL_SUPPLY = 1_000_000_000 * 10**18; // 1 billion tokens with 18 decimals

    // Token distribution
    uint256 public constant ECOSYSTEM_REWARD = 700_000_000 * 10**18; // 70% for ecosystem rewards
    uint256 public constant ECOSYSTEM_GROWTH = 200_000_000 * 10**18; // 20% for ecosystem growth
    uint256 public constant PUBLIC_GOODS = 100_000_000 * 10**18; // 10% for public goods

    // Vesting and rewards
    mapping(address => uint256) public lastRewardClaim;
    mapping(address => uint256) public stakedAmount;
    uint256 public constant REWARD_RATE = 100 * 10**18; // 100 tokens per day per staked token

    event TokensStaked(address indexed user, uint256 amount);
    event TokensUnstaked(address indexed user, uint256 amount);
    event RewardsClaimed(address indexed user, uint256 amount);

    constructor() ERC20(TOKEN_NAME, TOKEN_SYMBOL) {
        _mint(msg.sender, TOTAL_SUPPLY);
    }

    function stake(uint256 amount) external whenNotPaused {
        require(amount > 0, "Amount must be greater than 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        _transfer(msg.sender, address(this), amount);
        stakedAmount[msg.sender] += amount;
        lastRewardClaim[msg.sender] = block.timestamp;

        emit TokensStaked(msg.sender, amount);
    }

    function unstake(uint256 amount) external whenNotPaused {
        require(amount > 0, "Amount must be greater than 0");
        require(stakedAmount[msg.sender] >= amount, "Insufficient staked amount");

        stakedAmount[msg.sender] -= amount;
        _transfer(address(this), msg.sender, amount);

        emit TokensUnstaked(msg.sender, amount);
    }

    function claimRewards() external whenNotPaused {
        require(stakedAmount[msg.sender] > 0, "No staked tokens");
        
        uint256 timeStaked = block.timestamp - lastRewardClaim[msg.sender];
        uint256 rewards = (stakedAmount[msg.sender] * REWARD_RATE * timeStaked) / (1 days);
        
        require(rewards > 0, "No rewards available");
        require(balanceOf(address(this)) >= rewards, "Insufficient contract balance");

        lastRewardClaim[msg.sender] = block.timestamp;
        _transfer(address(this), msg.sender, rewards);

        emit RewardsClaimed(msg.sender, rewards);
    }

    function getPendingRewards(address user) external view returns (uint256) {
        if (stakedAmount[user] == 0) return 0;
        
        uint256 timeStaked = block.timestamp - lastRewardClaim[user];
        return (stakedAmount[user] * REWARD_RATE * timeStaked) / (1 days);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    function transferEcosystemRewards(address recipient, uint256 amount) external onlyOwner {
        require(amount <= ECOSYSTEM_REWARD, "Amount exceeds ecosystem reward allocation");
        _transfer(address(this), recipient, amount);
    }

    function transferEcosystemGrowth(address recipient, uint256 amount) external onlyOwner {
        require(amount <= ECOSYSTEM_GROWTH, "Amount exceeds ecosystem growth allocation");
        _transfer(address(this), recipient, amount);
    }

    function transferPublicGoods(address recipient, uint256 amount) external onlyOwner {
        require(amount <= PUBLIC_GOODS, "Amount exceeds public goods allocation");
        _transfer(address(this), recipient, amount);
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
} 