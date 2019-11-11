pragma solidity ^0.5;
pragma experimental ABIEncoderV2;
contract ImageLicense {

    Image[] images;


    enum Rights {
        FULL_RIGHTS,
        NON_PROFIT_REPLICATION,
        PROFIT_REPLICATION,
        NO_RIGHTS
    }

    struct Image {
        bytes image_binary;
        address owner;
        ImagePrice prices;
        mapping(address=>Rights) users_w_rights;
    }

    struct Proposal {
        uint offer;
        uint right;
    }

    struct ImagePrice {
        uint full_rights;
        uint non_profit;
        uint profit;
    }

    function setNewOwner (Image storage image, address new_owner) private {
        image.owner = new_owner;
    }

    function publishNewImage (bytes memory new_image, address owner, ImaePrice memory prices) public {
        Image memory image;
        image.image_binary = new_image;
        image.owner = owner;
        image.prices = prices;
        images.push(image);
    }

    function addUserRights (uint image_id, address user, Rights right) public {
        require(images[image_id].owner == msg.sender, "You have no rights to do this!");
        images[image_id].users_w_rights[user] = right;
    }

    function buyRights (uint image_id, Proposal offer) {
        require()
    }

    function payOwner (address owner, uint amount) {

    }


}

