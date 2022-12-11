/* HERE ARE ALL QUERIES USED RELATED TO THE PUBLISHER ADDITION */

-- Check if the publisher exists. If not, the return will give us nothing.
SELECT * 
FROM Publisher
WHERE {name} = Publisher.name

-- Get the highest pID (Publisher ID) so that we can considered the next publisher ID for this new publisher.
SELECT max(pID) 
FROM Publisher

-- Add to the publisher table the new publisher. Each {variable} is user input.
INSERT INTO Publisher 
VALUES({pID}, {name}, {address}, {contactEmail}, {accountNum}, {transitNum}, {institutionNum})

-- Since there can be multiple contact numbers, we add them to its own table.
INSERT INTO PublisherPhones 
VALUES({pID}, {number})