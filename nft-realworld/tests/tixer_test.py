
from brownie import accounts, Tixer
import brownie
import pytest
from scripts.helpful_scripts import get_account


def test_can_deploy():
    account = get_account()
    tixer = Tixer.deploy("TixerToken", "TXR", {"from": account})
    assert tixer is not None


def test_owner_is_set_correctly():
    account = get_account()
    tixer = Tixer.deploy("TixerToken", "TXR", {"from": account})
    assert tixer.owner() == account


def test_add_movie():
    account = accounts[0]
    tixer = Tixer.deploy("TixerToken", "TXR", {"from": account})

    movie_id = "some-random-guid"
    image = 'https://i0.wp.com/aiptcomics.com/wp-content/uploads/2022/12/AVENBEYOND2023001_Cov-1.jpg'
    movie_name = "Avengers Beyond"
    genre = "Action"
    price = 100
    tickets = 10
    max_tickets = 10
    cinemaArea = 1
    remarks = "Some remarks"
    time = "3pm-6pm"
    location = "Sm Fairview Cinemas"
    lftrbRatings = "R-16"

    # add movie test
    tixer.addMovies(movie_id, image, movie_name, genre, price, tickets, max_tickets, cinemaArea, remarks, time, location, lftrbRatings, {"from": account})
    movie = tixer.getMovies(movie_id)
    assert movie[2] == movie_name

    # assert only owner of the contract can perform an addMovie
    non_owner_account = accounts[1]
    with pytest.raises(brownie.exceptions.VirtualMachineError, match="Only the owner can perform this action"):
        tixer.addMovies(movie_id, image, movie_name, genre, price, tickets, max_tickets, cinemaArea, remarks, time, location, lftrbRatings, {"from": non_owner_account})



def test_mint_ticket():
    account = accounts[0]
    tixer = Tixer.deploy("TixerToken", "TXR", {"from": account})

    movie_id = "some-random-guid"
    image = 'https://static.wikia.nocookie.net/p__/images/8/85/Amazing_Spider-Man_Vol_3_10_Textless.jpg/revision/latest?cb=20180221185359&path-prefix=protagonist'
    movie_name = "Superior Spiderman"
    genre = "Action"
    price = 100
    tickets = 1 
    max_tickets = 1 
    cinemaArea = 1
    remarks = "Some remarks"
    time = "3pm-6pm"
    location = "Ayala malls"
    lftrbRatings = "R-18"
    tixer.addMovies(movie_id, image, movie_name, genre, price, tickets, max_tickets, cinemaArea, remarks, time, location, lftrbRatings, {"from": account})

    seat = "A1"
    tokenURI = "someTokenURI"
    value = price
    tixer.mintTicket(seat, movie_id, tokenURI, {"from": account, "value": value})

    ownerOfToken = tixer.ownerOf(tixer.totalSupply())
    seatOwner = tixer.seat(movie_id, seat)
    assert ownerOfToken == account
    assert seatOwner == account


def test_mint_ticket_is_soldout():
    account = accounts[0]
    tixer = Tixer.deploy("TixerToken", "TXR", {"from": account})

    movie_id = "some-random-guid"
    image = 'https://thathashtagshow.com/wp-content/uploads/2022/02/hulk-vs-thor-1280x640.jpg'
    movie_name = "Hulk vs Thor : Banner of War Alpha"
    genre = "Action"
    price = 100
    tickets = 1 
    max_tickets = 1 
    cinemaArea = 1
    remarks = "Some remarks"
    time = "3pm-6pm"
    location = "Robinsons"
    lftrbRatings = "R-18"
    tixer.addMovies(movie_id, image, movie_name, genre, price, tickets, max_tickets, cinemaArea, remarks,  time, location, lftrbRatings, {"from": account})

    seat = "A1"
    tokenURI = "someTokenURI"
    value = price
    tixer.mintTicket(seat, movie_id, tokenURI, {"from": account, "value": value})

    ownerOfToken = tixer.ownerOf(tixer.totalSupply())
    seatOwner = tixer.seat(movie_id, seat)
    assert ownerOfToken == account
    assert seatOwner == account

    with pytest.raises(brownie.exceptions.VirtualMachineError, match="Tickets are soldout"):
        for _ in range(tickets):
            tixer.mintTicket(seat, movie_id, tokenURI, {"from": account, "value": value})



def test_mint_ticket_is_not_enough_cash():
    account = accounts[0]
    tixer = Tixer.deploy("TixerToken", "TXR", {"from": account})

    movie_id = "some-random-guid"
    image = 'https://static.wikia.nocookie.net/p__/images/8/85/Amazing_Spider-Man_Vol_3_10_Textless.jpg/revision/latest?cb=20180221185359&path-prefix=protagonist'
    movie_name = "Superior Spiderman"
    genre = "Action"
    price = 100
    tickets = 1 
    max_tickets = 1 
    cinemaArea = 1
    remarks = "Some remarks"
    time = "3pm-6pm"
    location = "Ayala malls"
    lftrbRatings = "R-18"
    tixer.addMovies(movie_id, image, movie_name, genre, price, tickets, max_tickets, cinemaArea, remarks, time, location, lftrbRatings, {"from": account})

    seat = "A1"
    tokenURI = "someTokenURI"
    value = price

    with pytest.raises(brownie.exceptions.VirtualMachineError, match="Not enough cash"):
        tixer.mintTicket(seat, movie_id, tokenURI, {"from": account, "value": value -1})

    