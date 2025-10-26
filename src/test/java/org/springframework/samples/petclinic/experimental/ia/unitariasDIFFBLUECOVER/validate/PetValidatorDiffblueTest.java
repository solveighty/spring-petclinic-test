package org.springframework.samples.petclinic.owner;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import java.time.LocalDate;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.validation.BindException;
import org.springframework.validation.Errors;
import org.springframework.validation.FieldError;

class PetValidatorDiffblueTest {

	/**
	 * Test {@link PetValidator#validate(Object, Errors)}.
	 *
	 * <p>
	 * Method under test: {@link PetValidator#validate(Object, Errors)}
	 */
	@Test
	@DisplayName("Test validate(Object, Errors)")
	@Tag("MaintainedByDiffblue")
	void testValidate() {
		// Arrange
		PetValidator petValidator = new PetValidator();

		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(1);
		pet.setName("Bella");
		pet.setType(type);
		BindException errors = new BindException(pet, "org.springframework.samples.petclinic.owner.Pet");

		// Act
		petValidator.validate(pet, errors);

		// Assert that nothing has changed
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 0 errors",
				errors.getLocalizedMessage());
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 0 errors", errors.getMessage());
	}

	/**
	 * Test {@link PetValidator#validate(Object, Errors)}.
	 *
	 * <p>
	 * Method under test: {@link PetValidator#validate(Object, Errors)}
	 */
	@Test
	@DisplayName("Test validate(Object, Errors)")
	@Tag("MaintainedByDiffblue")
	void testValidate2() {
		// Arrange
		PetValidator petValidator = new PetValidator();

		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(null);
		pet.setId(1);
		pet.setName("Bella");
		pet.setType(type);
		BindException errors = new BindException(pet, "org.springframework.samples.petclinic.owner.Pet");

		// Act
		petValidator.validate(pet, errors);

		// Assert
		FieldError fieldError = errors.getFieldError();
		assertEquals("birthDate", fieldError.getField());
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 1 errors\n"
				+ "Field error in object 'org.springframework.samples.petclinic.owner.Pet' on field 'birthDate': rejected"
				+ " value [null]; codes [required.org.springframework.samples.petclinic.owner.Pet.birthDate,required"
				+ ".birthDate,required.java.time.LocalDate,required]; arguments []; default message [required]",
				errors.getLocalizedMessage());
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 1 errors\n"
				+ "Field error in object 'org.springframework.samples.petclinic.owner.Pet' on field 'birthDate': rejected"
				+ " value [null]; codes [required.org.springframework.samples.petclinic.owner.Pet.birthDate,required"
				+ ".birthDate,required.java.time.LocalDate,required]; arguments []; default message [required]",
				errors.getMessage());
		String[] codes = fieldError.getCodes();
		assertEquals("required.birthDate", codes[1]);
		assertEquals("required.java.time.LocalDate", codes[2]);
		assertEquals("required.org.springframework.samples.petclinic.owner.Pet.birthDate", codes[0]);
		assertNull(fieldError.getRejectedValue());
		assertEquals(4, codes.length);
	}

	/**
	 * Test {@link PetValidator#validate(Object, Errors)}.
	 *
	 * <p>
	 * Method under test: {@link PetValidator#validate(Object, Errors)}
	 */
	@Test
	@DisplayName("Test validate(Object, Errors)")
	@Tag("MaintainedByDiffblue")
	void testValidate3() {
		// Arrange
		PetValidator petValidator = new PetValidator();

		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(1);
		pet.setName("");
		pet.setType(type);
		BindException errors = new BindException(pet, "org.springframework.samples.petclinic.owner.Pet");

		// Act
		petValidator.validate(pet, errors);

		// Assert
		FieldError fieldError = errors.getFieldError();
		assertEquals("", fieldError.getRejectedValue());
		assertEquals("name", fieldError.getField());
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 1 errors\n"
				+ "Field error in object 'org.springframework.samples.petclinic.owner.Pet' on field 'name': rejected value"
				+ " []; codes [required.org.springframework.samples.petclinic.owner.Pet.name,required.name,required.java"
				+ ".lang.String,required]; arguments []; default message [required]", errors.getLocalizedMessage());
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 1 errors\n"
				+ "Field error in object 'org.springframework.samples.petclinic.owner.Pet' on field 'name': rejected value"
				+ " []; codes [required.org.springframework.samples.petclinic.owner.Pet.name,required.name,required.java"
				+ ".lang.String,required]; arguments []; default message [required]", errors.getMessage());
		String[] codes = fieldError.getCodes();
		assertEquals("required.java.lang.String", codes[2]);
		assertEquals("required.name", codes[1]);
		assertEquals("required.org.springframework.samples.petclinic.owner.Pet.name", codes[0]);
		assertEquals(4, codes.length);
	}

	/**
	 * Test {@link PetValidator#validate(Object, Errors)}.
	 *
	 * <ul>
	 * <li>When {@link Pet} (default constructor) Id is {@code null}.
	 * </ul>
	 *
	 * <p>
	 * Method under test: {@link PetValidator#validate(Object, Errors)}
	 */
	@Test
	@DisplayName("Test validate(Object, Errors); when Pet (default constructor) Id is 'null'")
	@Tag("MaintainedByDiffblue")
	void testValidate_whenPetIdIsNull() {
		// Arrange
		PetValidator petValidator = new PetValidator();

		PetType type = new PetType();
		type.setId(1);
		type.setName("Dog");

		Pet pet = new Pet();
		pet.setBirthDate(LocalDate.of(1970, 1, 1));
		pet.setId(null);
		pet.setName("Bella");
		pet.setType(type);
		BindException errors = new BindException(pet, "org.springframework.samples.petclinic.owner.Pet");

		// Act
		petValidator.validate(pet, errors);

		// Assert that nothing has changed
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 0 errors",
				errors.getLocalizedMessage());
		assertEquals("org.springframework.validation.BeanPropertyBindingResult: 0 errors", errors.getMessage());
	}

}
