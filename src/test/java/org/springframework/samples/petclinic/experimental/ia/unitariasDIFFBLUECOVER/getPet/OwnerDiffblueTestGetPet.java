package org.springframework.samples.petclinic.owner;

import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.time.LocalDate;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class OwnerGetPetDiffblueTest {

	/**
	 * Test {@link Owner#getPets()}.
	 *
	 * <p>
	 * Method under test: {@link Owner#getPets()}
	 */
	@Test
	@DisplayName("Test getPets()")
	@Tag("MaintainedByDiffblue")
	void testGetPets() {
		// Arrange, Act and Assert
		assertTrue(new Owner().getPets().isEmpty());
	}

	/**
	 * Test {@link Owner#getPet(Integer)} with {@code id}.
	 *
	 * <ul>
	 * <li>Given {@link Owner} (default constructor).
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(Integer)}
	 */
	@Test
	@DisplayName("Test getPet(Integer) with 'id'; given Owner (default constructor)")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithId_givenOwner() {
		// Arrange, Act and Assert
		assertNull(new Owner().getPet(1));
	}

	/**
	 * Test {@link Owner#getPet(Integer)} with {@code id}.
	 *
	 * <ul>
	 * <li>Given {@link PetType} (default constructor) Id is one.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(Integer)}
	 */
	@Test
	@DisplayName("Test getPet(Integer) with 'id'; given PetType (default constructor) Id is one")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithId_givenPetTypeIdIsOne() {
		// Arrange
		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Bella");
		pet.setType(type);

		Owner owner = new Owner();
		owner.addPet(pet);

		// Act and Assert
		assertNull(owner.getPet(1));
	}

	/**
	 * Test {@link Owner#getPet(String, boolean)} with {@code name}, {@code ignoreNew}.
	 *
	 * <ul>
	 * <li>Given {@link Owner} (default constructor).
	 * <li>When {@code true}.
	 * <li>Then return {@code null}.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String, boolean)}
	 */
	@Test
	@DisplayName("Test getPet(String, boolean) with 'name', 'ignoreNew'; given Owner (default constructor); when 'true'; then return 'null'")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithNameIgnoreNew_givenOwner_whenTrue_thenReturnNull() {
		// Arrange, Act and Assert
		assertNull(new Owner().getPet("Bella", true));
	}

	/**
	 * Test {@link Owner#getPet(String, boolean)} with {@code name}, {@code ignoreNew}.
	 *
	 * <ul>
	 * <li>Given {@link Pet} (default constructor) Name is {@code Bella}.
	 * <li>When {@code false}.
	 * <li>Then return {@link Pet} (default constructor).
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String, boolean)}
	 */
	@Test
	@DisplayName("Test getPet(String, boolean) with 'name', 'ignoreNew'; given Pet (default constructor) Name is 'Bella'; when 'false'; then return Pet (default constructor)")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithNameIgnoreNew_givenPetNameIsBella_whenFalse_thenReturnPet() {
		// Arrange
		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Bella");
		pet.setType(type);

		Owner owner = new Owner();
		owner.addPet(pet);

		// Act and Assert
		assertSame(pet, owner.getPet("Bella", false));
	}

	/**
	 * Test {@link Owner#getPet(String, boolean)} with {@code name}, {@code ignoreNew}.
	 *
	 * <ul>
	 * <li>Given {@link Pet} (default constructor) Name is {@code Bella}.
	 * <li>When {@code true}.
	 * <li>Then return {@code null}.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String, boolean)}
	 */
	@Test
	@DisplayName("Test getPet(String, boolean) with 'name', 'ignoreNew'; given Pet (default constructor) Name is 'Bella'; when 'true'; then return 'null'")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithNameIgnoreNew_givenPetNameIsBella_whenTrue_thenReturnNull() {
		// Arrange
		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Bella");
		pet.setType(type);

		Owner owner = new Owner();
		owner.addPet(pet);

		// Act and Assert
		assertNull(owner.getPet("Bella", true));
	}

	/**
	 * Test {@link Owner#getPet(String, boolean)} with {@code name}, {@code ignoreNew}.
	 *
	 * <ul>
	 * <li>Given {@link Pet} (default constructor) Name is {@code Name}.
	 * <li>When {@code true}.
	 * <li>Then return {@code null}.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String, boolean)}
	 */
	@Test
	@DisplayName("Test getPet(String, boolean) with 'name', 'ignoreNew'; given Pet (default constructor) Name is 'Name'; when 'true'; then return 'null'")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithNameIgnoreNew_givenPetNameIsName_whenTrue_thenReturnNull() {
		// Arrange
		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Name");
		pet.setType(type);

		Owner owner = new Owner();
		owner.addPet(pet);

		// Act and Assert
		assertNull(owner.getPet("Bella", true));
	}

	/**
	 * Test {@link Owner#getPet(String)} with {@code name}.
	 *
	 * <ul>
	 * <li>Given {@link Owner} (default constructor).
	 * <li>Then return {@code null}.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String)}
	 */
	@Test
	@DisplayName("Test getPet(String) with 'name'; given Owner (default constructor); then return 'null'")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithName_givenOwner_thenReturnNull() {
		// Arrange, Act and Assert
		assertNull(new Owner().getPet("Bella"));
	}

	/**
	 * Test {@link Owner#getPet(String)} with {@code name}.
	 *
	 * <ul>
	 * <li>Given {@link Pet} (default constructor) Name is {@code Bella}.
	 * <li>Then return {@link Pet} (default constructor).
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String)}
	 */
	@Test
	@DisplayName("Test getPet(String) with 'name'; given Pet (default constructor) Name is 'Bella'; then return Pet (default constructor)")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithName_givenPetNameIsBella_thenReturnPet() {
		// Arrange
		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Bella");
		pet.setType(type);

		Owner owner = new Owner();
		owner.addPet(pet);

		// Act and Assert
		assertSame(pet, owner.getPet("Bella"));
	}

	/**
	 * Test {@link Owner#getPet(String)} with {@code name}.
	 *
	 * <ul>
	 * <li>Given {@link Pet} (default constructor) Name is {@code Name}.
	 * <li>Then return {@code null}.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link Owner#getPet(String)}
	 */
	@Test
	@DisplayName("Test getPet(String) with 'name'; given Pet (default constructor) Name is 'Name'; then return 'null'")
	@Tag("MaintainedByDiffblue")
	void testGetPetWithName_givenPetNameIsName_thenReturnNull() {
		// Arrange
		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Name");
		pet.setType(type);

		Owner owner = new Owner();
		owner.addPet(pet);

		// Act and Assert
		assertNull(owner.getPet("Bella"));
	}

}
