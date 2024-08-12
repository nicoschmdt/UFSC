pragma solidity ^0.5;
pragma experimental ABIEncoderV2;

contract ImageLicense {

    Image[] public images;
    mapping(address => uint) balances;
    uint image_id_counter = 0;

    enum Rights {
        FULL_RIGHTS,
        NON_PROFIT_REPLICATION,
        PROFIT_REPLICATION
    }

    struct Image {
        uint image_id;
        bytes image_binary;
        address owner;
        LicensePrices prices;
        mapping(address => Rights) users_ledger;
    }

    struct Proposal {
        Rights right;
        uint amount;
    }

    struct LicensePrices {
        uint full_rights;
        uint non_profit;
        uint profit;
    }

    function publishNewImage (bytes memory new_image) public {
        images.push(Image(image_id_counter, new_image, msg.sender, LicensePrices(0, 0, 0)));
        image_id_counter++;
    }

    function setLicensePricing (uint image_id, LicensePrices memory _prices) public {
        require(images[image_id].owner == msg.sender, "Only the owner can change the pricing");
        images[image_id].prices = _prices;
    }

    function buyLicense (uint image_id, Proposal memory offer) public {
        verifyPayment(image_id, offer);
        payOwner(image_id, offer);
        addUserRights(image_id, offer.right);
    }

    function donateToArtist (uint image_id, uint amount) public {
        require(balances[msg.sender] >= amount, "You don't have enough to this donation");
        balances[images[image_id].owner] += amount;
        balances[msg.sender] -= amount;
    }

    function verifyPayment (uint image_id, Proposal memory offer) private {
        if(offer.right == Rights.FULL_RIGHTS) {
            require(offer.amount >= images[image_id].prices.full_rights, "You have to pay the desired amount for full rights");
        } else if(offer.right == Rights.NON_PROFIT_REPLICATION) {
            require(offer.amount >= images[image_id].prices.non_profit, "You have to pay the desired amount for non profitable rights");
        } else if(offer.right == Rights.PROFIT_REPLICATION) {
            require(offer.amount >= images[image_id].prices.profit, "You have to pay the desired amount for profitable rights");
        }
    }

    function payOwner (uint image_id, Proposal memory offer) private {
        balances[images[image_id].owner] += offer.amount;
        balances[msg.sender] -= offer.amount;
    }

    function addUserRights (uint image_id, Rights right) private {
        address user = msg.sender;
        if(right == Rights.FULL_RIGHTS) {
            images[image_id].owner = user;
        }

        images[image_id].users_ledger[user] = right;
    }
}
