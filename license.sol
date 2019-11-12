pragma solidity ^0.5;
pragma experimental ABIEncoderV2;

contract ImageLicense {

    Image[] public images;

    enum Rights {
        FULL_RIGHTS,
        NON_PROFIT_REPLICATION,
        PROFIT_REPLICATION
    }

    struct Image {
        bytes image_binary;
        Person owner;
        LicensePrices prices;
        mapping(address => Rights) users_ledger;
    }

    struct Proposal {
        Person buyer;
        Rights right;
        uint amount;
    }

    struct Person {
        address _person;
        uint wallet;
    }

    struct LicensePrices {
        uint full_rights;
        uint non_profit;
        uint profit;
    }

    function publishNewImage (bytes memory new_image, Person memory artist) public {
        images.push(Image(new_image, artist, LicensePrices(0, 0, 0)));
    }

    function setLicensePricing (uint image_id, LicensePrices memory _prices) public {
        require(images[image_id].owner._person == msg.sender, "Only the owner can change the pricing");
        images[image_id].prices = _prices
    }

    function buyLicense (uint image_id, Proposal memory offer) public {
        verifyPayment(image_id, offer);
        payOwner(image_id, offer);
        addUserRights(image_id, offer.buyer, offer.right);
    }

    function donateToArtist (uint image_id, Proposal donation) public {
        images[image_id].owner.wallet += donation.amount;
        donation.buyer.wallet -= donation.amount;
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
        images[image_id].owner.wallet += offer.amount;
        offer.buyer.wallet -= offer.amount;
    }

    function addUserRights (uint image_id, Person memory user, Rights right) private {
        if(right == Rights.FULL_RIGHTS) {
            images[image_id].owner = user;
        }

        images[image_id].users_ledger[user._person] = right;
    }
}

