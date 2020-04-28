pragma solidity 0.4.24;

contract Factus { 
    address private owner;
    struct Report{
        string reporter;
        string lawyer;
        string reporterInfo;
        string desc;
        string RIkey;
        string DESCkey;
    }
    
    mapping(string => Report) private reports; 
    mapping(string => bool) private isExist;
    constructor(address _owner) public {
        owner = _owner;
    }
    
    modifier onlyOwner {
        require(msg.sender==owner);
        _;
    }
    
    function addReport (string memory _id, string memory _reporter, string memory _lawyer,
    string memory _reporterInfo, string memory _desc, 
    string memory _RIkey, string memory _DESCkey) onlyOwner public {
        require(!isExist[_id]);
        reports[_id] = Report({reporter: _reporter, lawyer: _lawyer, reporterInfo: _reporterInfo,
            desc: _desc, RIkey: _RIkey, DESCkey: _DESCkey});
	    isExist[_id] = true;
    }

    function deleteLawyer(string memory _id, string memory _lawyer) onlyOwner public {
        require(isExist[_id], "wrong report id");
        Report memory report = reports[_id];
        require(keccak256(bytes(report.lawyer))==keccak256(bytes(_lawyer)), "wrong user");
        report.lawyer = "";
    }
    
    function assignLawyer(string memory _id, string memory _lawyer) onlyOwner public {
        require(isExist[_id] && bytes(reports[_id].lawyer).length == 0); 
        reports[_id].lawyer = _lawyer;
    }
    
    function getRIkey(string memory _id, string memory _user, string memory _hashedData) onlyOwner public returns (string memory){
        require(isExist[_id], "wrong report id");
        Report memory report = reports[_id];
        require(keccak256(bytes(report.lawyer))==keccak256(bytes(_user)), "wrong user");
        emit GetRI(now, "get RI key");
        emit CheckHash(keccak256(bytes(report.reporterInfo)) == keccak256(bytes(_hashedData)));
        return report.RIkey;
    }
    
    function getDESCkey(string memory _id, string memory _user, string memory _hashedData) onlyOwner public returns (string memory){
        require(isExist[_id], "wrong report id");
        Report memory report = reports[_id];
        require(keccak256(bytes(report.reporter))==keccak256(bytes(_user))||keccak256(bytes(report.lawyer))==keccak256(bytes(_user)), "wrong user");
        require(keccak256(bytes(report.desc)) == keccak256(bytes(_hashedData)), "server data is changed");
        string memory user= "";
        
        if (keccak256(bytes(report.reporter))==keccak256(bytes(_user))){
            user = "reporter";
        }
        else user = "lawyer";
        
        emit GetDesc(user, now, report.DESCkey);
        emit CheckHash(keccak256(bytes(report.desc)) == keccak256(bytes(_hashedData)));
        return report.DESCkey;
    }
    
    event GetDesc(string user, uint _time, string msg);
    event GetRI(uint _time, string msg);
    event CheckHash(bool check);

}