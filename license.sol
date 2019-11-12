pragma solidity ^0.5;
pragma experimental ABIEncoderV2;
contract ImageLicense {

    Image[] public images;


    enum Rights {
        FULL_RIGHTS,
        NON_PROFIT_REPLICATION,
        PROFIT_REPLICATION,
        NO_RIGHTS
    }

    struct Image {
        bytes image_binary;
        Person owner;
        ImagePrice prices;
        mapping(address=>Rights) users_w_rights;
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

    struct ImagePrice {
        uint full_rights;
        uint non_profit;
        uint profit;
    }

    function publishNewImage (bytes memory new_image, Person memory owner, ImagePrice memory prices) public {
        images.push(Image(new_image, owner, prices));
    }

    function buyRights (uint image_id, Proposal memory offer) public {
        if(offer.right == Rights.FULL_RIGHTS) {
            require(offer.amount >= images[image_id].prices.full_rights, "You have to pay the desired amount for full rights");
        } else if(offer.right == Rights.NON_PROFIT_REPLICATION) {
            require(offer.amount >= images[image_id].prices.non_profit, "You have to pay the desired amount for non profitable rights");
        } else if(offer.right == Rights.PROFIT_REPLICATION) {
            require(offer.amount >= images[image_id].prices.profit, "You have to pay the desired amount for profitable rights");
        }

        payOwner(image_id, offer);
        addUserRights(image_id, offer.buyer, offer.right);
    }

    function addUserRights (uint image_id, Person memory user, Rights right) private {
        if(right == Rights.FULL_RIGHTS) {
            images[image_id].owner = user;
        }

        images[image_id].users_w_rights[user._person] = right;
    }

    function payOwner (uint image_id, Proposal memory offer) private {
        images[image_id].owner.wallet += offer.amount;
        offer.buyer.wallet -= offer.amount;
    }


}

