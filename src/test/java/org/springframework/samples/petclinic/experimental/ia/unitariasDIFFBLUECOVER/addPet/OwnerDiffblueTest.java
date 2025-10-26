package org.springframework.samples.petclinic.owner;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class OwnerAddPetDiffblueTest {

	/**
	 * Test {@link Owner#addPet(Pet)}.
	 *
	 * <ul>
	 * <li>Given {@code null}.
	 * <li>When {@link Pet} (default constructor) Id is {@code null}.
	 * <li>Then {@link Owner} (default constructor) Pets size is one.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#addPet(Pet)}
	 */
	@Test
	@DisplayName("Test addPet(Pet); given 'null'; when Pet (default constructor) Id is 'null'; then Owner (default constructor) Pets size is one")
	@Tag("MaintainedByDiffblue")
	void testAddPet_givenNull_whenPetIdIsNull_thenOwnerPetsSizeIsOne() {
		// Arrange
		Owner owner = new Owner();

		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Bella");
		pet.setType(type);

		// Act
		owner.addPet(pet);

		// Assert
		List<Pet> pets = owner.getPets();
		assertEquals(1, pets.size());
		assertSame(pet, pets.get(0));
	}

	/**
	 * Test {@link Owner#addPet(Pet)}.
	 *
	 * <ul>
	 * <li>Given one.
	 * <li>When {@link Pet} (default constructor) Id is one.
	 * <li>Then {@link Owner} (default constructor) Pets Empty.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#addPet(Pet)}
	 */
	@Test
	@DisplayName("Test addPet(Pet); given one; when Pet (default constructor) Id is one; then Owner (default constructor) Pets Empty")
	@Tag("MaintainedByDiffblue")
	void testAddPet_givenOne_whenPetIdIsOne_thenOwnerPetsEmpty() {
		// Arrange
		Owner owner = new Owner();

		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(1);
		pet.setName("Bella");
		pet.setType(type);

		// Act
		owner.addPet(pet);

		// Assert that nothing has changed
		assertTrue(owner.getPets().isEmpty());
	}

}
